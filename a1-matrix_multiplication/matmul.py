def matrix_multiply(matrix1, matrix2):
    """
    Function to carry matrix multiplication
    inputs:- 2 variables which are list of lists or similar data type being treated as matrices
    output:- result of matrix multiplication ( martix1*matrix2 ) as a list of list
    raising errors if input isnt ideal to the programe
    to handle floating point values it is being rounded off to 3 decimal places
    """
    flag = False  # setting up a flag to handle errors
    if len(matrix1) == 0:  # checking for empty matrices
        flag = True
        raise ValueError
    else:
        if len(matrix2) == 0:  # checking for empty matrices
            flag = True
            raise ValueError
        else:
            col1 = len(matrix1[0])
            row1 = len(matrix1)
            col2 = len(matrix2[0])
            row2 = len(matrix2)

            len_element1 = matrix1[0]
            len_element2 = matrix2[0]
            for i in matrix1:
                if len(i) != len_element1:
                    flag = True
            for i in matrix2:
                if len(i) != len_element2:
                    flag = True

            if col1 != row2:  # checking row = coloumn
                flag = True
                raise ValueError
            else:
                if not flag:
                    # starting the main program
                    result_matrix = list()  # stores the result
                    for i in range(row1):  # iterating on the rows
                        row_vector = list()  # stores the result of the multiplication
                        for j in range(col2):  # iterating on the coloumns
                            sum = 0
                            for k in range(row2):  # multiplying the elements
                                aij = matrix1[i][k]
                                bji = matrix2[k][j]
                                if (
                                    type(aij) != int and type(bji) != int
                                ):  # checking for the type of the elements
                                    flag = True
                                else:
                                    # rounding of floating point numbers
                                    if type(aij) == float:
                                        aij = round(aij, 3)
                                    if type(bji) == float:
                                        bji = round(bji, 3)
                                    sum += aij * bji
                            row_vector.append(sum)
                        result_matrix.append(row_vector)

    if flag:  # if an error flag has been raised
        raise NotImplementedError("Matrix multiplication function not implemented")
    else:
        return result_matrix  # if there's no error then return the result
