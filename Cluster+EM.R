library(mvtnorm)
library(ggplot2)


sigma_func<-function(myX,mu,y,q,NK){
  vari=array(0,dim=c(dim(myX)[2],dim(myX)[2],K))
  for(ii in 1:K){
    temp = matrix(0,dim(myX)[2],dim(myX)[2])
    for(jj in 1:dim(myX)[1]){
      temp = temp+(myX[jj,]-mu[ii,])%*%t(myX[jj,]-mu[ii,])*y[jj,ii]
    }
    vari[,,ii]=temp/NK[ii]
    svd1=svd(vari[,,ii])
    SQ = 1/(dim(myX)[2]-q)*sum(svd1$d[(q+1):dim(myX)[2]])
    if(q==0){
      sigma[,,ii]=SQ*diag(1,dim(myX)[2],dim(myX)[2])
    }else{
      WQ = svd1$v[,1:q]%*%diag(apply(as.matrix(svd1$d[1:q]),1,function(xx){
        return(sqrt(xx-SQ))}),q,q)
      sigma[,,ii] = WQ%*%t(WQ)+SQ*diag(1,dim(myX)[2],dim(myX)[2])
    }
  }
  return(sigma)
}


likelihood_func<-function(myX,mu,sigma,pi){
  temp = matrix(0,dim(myX)[1],K)
  for(ii in 1:K){
    temp[,ii] = dmvnorm(myX, mean = mu[ii,], sigma = sigma[,,ii])
  }
  likelihood = sum(log(temp%*%pi))
  return(likelihood)
}



misRate_func<-function(myX,myLabel,EMLabel,K){
  misRate = matrix(1,K+1,1)
  temp1 = 0
  for (ii in 1:K){
    temp = apply(EMLabel[myLabel==(ii-1),],2,function(xx){
      return(sum(xx))})
    misRate[ii,] = 1-max(temp)/sum(temp)
    temp1 = temp1+max(temp)
  }
  OverAllMisRate = 1-temp1/dim(myX)[1]
  misRate = misRate*100
  OverAllMisRate = OverAllMisRate*100
  misRate[ii+1,]=OverAllMisRate
  cat("\n","misRate=",misRate[1:K]," ","OverAllMisRate=",misRate[K+1])
  return(misRate)
}


EM_func<-function(myX,K,mu,pi,q){
  sigma=sigma_func(myX,mu,y,q,NK)
  old_likelihood=likelihood_func(myX,mu,sigma,pi)
  mylikelihood=old_likelihood
  continueLoop = TRUE
  iter = 0
  while(continueLoop){
    # E step
    temp = matrix(0,dim(myX)[1],K)
    for(ii in 1:K){
      temp[,ii] = dmvnorm(myX, mean = mu[ii,], sigma = sigma[,,ii])*pi[ii]
    }
    cond = t(apply(temp,1,function(xx){
      return(xx/sum(xx))
    }))
    # M step
    N = apply(cond,2,function(xx){
      return(sum(xx))
    })
    pi=t(t(N)/dim(myX)[1])
    mu= t(cond)%*%myX/N
    sigma=sigma_func(myX,mu,cond,q,N)
    loglikelihood=likelihood_func(myX,mu,sigma,pi)
    if(abs((loglikelihood-old_likelihood)/loglikelihood)<0.00001){
      continueLoop = FALSE
    }
    old_likelihood=loglikelihood
    mylikelihood = rbind(mylikelihood,old_likelihood)
    iter=iter+1
    cat("\n","iteration number=",iter," ","likelihood=",loglikelihood)
  }
  
  df=data.frame(iteration=1:(iter+1),mylikelihood)
  p1=ggplot(df,aes(x=iteration,y=mylikelihood))+ geom_point()+ ggtitle(bquote(paste("q=",.(q)))) 
  # compute AIC
  AIC = -2*old_likelihood+2*(dim(myX)[2]*q-q*(q-1)/2)
  cat("\n","q=",q," ","AIC=",AIC)

  return(list(cond_fun=cond,pt=p1,mu=mu,sigma=sigma))
}


#rep(1,51),rep(2,45),rep(3,48),rep(4,44),rep(5,44),rep(6,42),rep(7,47),
# Read data
myX=read.table("C:/users/dawei/downloads/test2.txt",header=FALSE,sep=',')
myLabel=c(rep(1,31),rep(2,42),rep(3,51),rep(4,51),rep(5,52),rep(6,49),rep(7,51))


#pcmp<-prcomp(myX, center = TRUE) 

#tt=predict(pcmp)[,1:50]
#myX=scale(myX,pcmp$center,pcmp$scale)%*%pcmp$rotation[,1:50]



K=7
PreKmean<-kmeans(myX,K)
Clusters=PreKmean$cluster
ClusterMean=PreKmean$centers
y=matrix(0,dim(myX)[1],7)
for(i in 1:dim(myX)[1]){
  y[i,Clusters[i]]=1
}
mu=ClusterMean
pi=apply(y,2,function(n){return(sum(n)/dim(myX)[1])})
sigma=array(0,dim=c(dim(myX)[2],dim(myX)[2],K))
NK=pi*dim(myX)[1]

#initial accuracy
misRate<-misRate_func(myX,myLabel,y,K)
#visualize accuracy
barplot(t(misRate[1:7,]),names.arg = c("0", "1", "2","3", "4", "5","6"),xlab="hand-written digits", ylab="miscategorization
          rate %", main=paste("Overall mis-categorization rate = ", round(misRate[8,], digits = 2)))
box()


cond1=EM_func(myX,K,mu,pi,0)
cond2=EM_func(myX,K,mu,pi,4)

multiplot(cond1$pt, cond2$pt, cond3$pt, cond4$pt,cols=2)

dev.new(width=6, height=10)
par(mai=c(0,0,0,0),cex=0.8,mfrow=c(10,6))
myDraw = array(0,dim=c(6,dim(myX)[2],K))
clusterMean = cond2$mu
for(ii in 1:K){
  myDraw[1,,ii] = clusterMean[ii,]
  myDraw[2:6,,ii] = rmvnorm(n=5,mean=cond2$mu[ii,],sigma=cond2$sigma[,,ii])
}
for(ii in 1:K){
  for(jj in 1:6){
    image(t(matrix(myDraw[jj,,ii],byrow=TRUE,16,16)[16:1,]),col=gray(0:128/128),axes=FALSE)
    box()
  }
}


# calculate new Labels
EMLabel = matrix(0,dim(myX)[1],K)
for(ii in 1:dim(myX)[1]){
  EMLabel[ii,which.max(cond2$cond_fun[ii,])] = 1
}
misRate<-misRate_func(myX,myLabel,EMLabel,K)
barplot(t(misRate[1:7,]),names.arg = c("0", "1", "2","3", "4", "5","6"),xlab="hand-written digits", ylab="miscategorization
        rate%", main=paste("Overall mis-categorization rate = ", round(misRate[8], digits = 2), "% (q=",6,")"))
box()

myX1=read.table("C:/users/dawei/downloads/test2.txt",header=FALSE,sep=',')
mylabel1=c(rep(1,51),rep(2,45),rep(3,48),rep(4,44),rep(5,44),rep(6,42),rep(7,47))

write.csv(mu,row.names = FALSE,'E:/A+GTCLASS/mu.csv')
