"""
Matrix square root for general matrices and for upper triangular matrices.

This module exists to avoid cyclic imports.

"""
from __future__ import division, print_function, absolute_import

__all__ = ['sqrtm']

import numpy as np


# Local imports
from .misc import norm
from .lapack import ztrsyl, dtrsyl
from .decomp_schur import schur, rsf2csf


class SqrtmError(np.linalg.LinAlgError):
    pass


def _sqrtm_triu(T, blocksize=64):
    """
    Matrix square root of an upper triangular matrix.

    This is a helper function for `sqrtm` and `logm`.

    Parameters
    ----------
    T : (N, N) array_like upper triangular
        Matrix whose square root to evaluate
    blocksize : int, optional
        If the blocksize is not degenerate with respect to the
        size of the input array, then use a blocked algorithm. (Default: 64)

    Returns
    -------
    sqrtm : (N, N) ndarray
        Value of the sqrt function at `T`

    References
    ----------
    .. [1] Edvin Deadman, Nicholas J. Higham, Rui Ralha (2013)
           "Blocked Schur Algorithms for Computing the Matrix Square Root,
           Lecture Notes in Computer Science, 7782. pp. 171-182.

    """
    T_diag = np.diag(T)
    keep_it_real = np.isrealobj(T) and np.min(T_diag) >= 0
    if not keep_it_real:
        T_diag = T_diag.astype(complex)
    R = np.diag(np.sqrt(T_diag))

    # Compute the number of blocks to use; use at least one block.
    n, n = T.shape
    nblocks = max(n // blocksize, 1)

    # Compute the smaller of the two sizes of blocks that
    # we will actually use, and compute the number of large blocks.
    bsmall, nlarge = divmod(n, nblocks)
    blarge = bsmall + 1
    nsmall = nblocks - nlarge
    if nsmall * bsmall + nlarge * blarge != n:
        raise Exception('internal inconsistency')

    # Define the index range covered by each block.
    start_stop_pairs = []
    start = 0
    for count, size in ((nsmall, bsmall), (nlarge, blarge)):
        for i in range(count):
            start_stop_pairs.append((start, start + size))
            start += size

    # Within-block interactions.
    for start, stop in start_stop_pairs:
        for j in range(start, stop):
            for i in range(j-1, start-1, -1):
                s = 0
                if j - i > 1:
                    s = R[i, i+1:j].dot(R[i+1:j, j])
                denom = R[i, i] + R[j, j]
                if not denom:
                    raise SqrtmError('failed to find the matrix square root')
                R[i,j] = (T[i,j] - s) / denom

    # Between-block interactions.
    for j in range(nblocks):
        jstart, jstop = start_stop_pairs[j]
        for i in range(j-1, -1, -1):
            istart, istop = start_stop_pairs[i]
            S = T[istart:istop, jstart:jstop]
            if j - i > 1:
                S = S - R[istart:istop, istop:jstart].dot(
                        R[istop:jstart, jstart:jstop])

            # Invoke LAPACK.
            # For more details, see the solve_sylvester implemention
            # and the fortran dtrsyl and ztrsyl docs.
            Rii = R[istart:istop, istart:istop]
            Rjj = R[jstart:jstop, jstart:jstop]
            if keep_it_real:
                x, scale, info = dtrsyl(Rii, Rjj, S)
            else:
                x, scale, info = ztrsyl(Rii, Rjj, S)
            R[istart:istop, jstart:jstop] = x * scale

    # Return the matrix square root.
    return R


def sqrtm(A, disp=True, blocksize=64):
    """
    Matrix square root.

    Parameters
    ----------
    A : (N, N) array_like
        Matrix whose square root to evaluate
    disp : bool, optional
        Print warning if error in the result is estimated large
        instead of returning estimated error. (Default: True)
    blocksize : integer, optional
        If the blocksize is not degenerate with respect to the
        size of the input array, then use a blocked algorithm. (Default: 64)

    Returns
    -------
    sqrtm : (N, N) ndarray
        Value of the sqrt function at `A`

    errest : float
        (if disp == False)

        Frobenius norm of the estimated error, ||err||_F / ||A||_F

    References
    ----------
    .. [1] Edvin Deadman, Nicholas J. Higham, Rui Ralha (2013)
           "Blocked Schur Algorithms for Computing the Matrix Square Root,
           Lecture Notes in Computer Science, 7782. pp. 171-182.

    Examples
    --------
    >>> from scipy.linalg import sqrtm
    >>> a = np.array([[1.0, 3.0], [1.0, 4.0]])
    >>> r = sqrtm(a)
    >>> r
    array([[ 0.75592895,  1.13389342],
           [ 0.37796447,  1.88982237]])
    >>> r.dot(r)
    array([[ 1.,  3.],
           [ 1.,  4.]])

    """
    A = np.asarray(A)
    if len(A.shape) != 2:
        raise ValueError("Non-matrix input to matrix function.")
    if blocksize < 1:
        raise ValueError("The blocksize should be at least 1.")
    keep_it_real = np.isrealobj(A)
    if keep_it_real:
        T, Z = schur(A)
        if not np.array_equal(T, np.triu(T)):
            T, Z = rsf2csf(T,Z)
    else:
        T, Z = schur(A, output='complex')
    failflag = False
    try:
        R = _sqrtm_triu(T, blocksize=blocksize)
        ZH = np.conjugate(Z).T
        X = Z.dot(R).dot(ZH)
    except SqrtmError as e:
        failflag = True
        X = np.empty_like(A)
        X.fill(np.nan)

    if disp:
        nzeig = np.any(np.diag(T) == 0)
        if nzeig:
            print("Matrix is singular and may not have a square root.")
        elif failflag:
            print("Failed to find a square root.")
        return X
    else:
        try:
            arg2 = norm(X.dot(X) - A,'fro')**2 / norm(A,'fro')
        except ValueError:
            # NaNs in matrix
            arg2 = np.inf

        return X, arg2
