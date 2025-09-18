import numpy as np
def evalSpice(filename):

    if len(filename)==0: #empty file
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')
    else:
        if filename[-4:] != '.ckt':
            raise FileNotFoundError('Please give the name of a valid SPICE file as input')
        
    fptr=open(filename,'r')
    flag=True

    for i in fptr:
        if i == ".circuit\n": #this signals the start of the circuit
            flag=False
            break 
    
    if flag:
        #the circuit was not read
        raise ValueError('Malformed circuit file')

    # key is the node and value is a list of tuples, the tuples contain connected branch and the component in that connection 
    #(connected node, component)
    node_connections=dict() 

    #to store the components in the (a,b) branch with current flowing from a to b or the voltage
    branch_components=dict()    

    ascending_list_of_nodes=list()
    aux_eqns=0
    aux_list=list()

    storage=fptr.readlines() # all the lines of the circuit being read and checking if it ends
    print(storage) 
    if ".end\n" not in storage:
        raise ValueError('Malformed circuit file')

    valid_components=["V","I","R"]
    i=0 # used in the following while loop and is used to traverse the list storage 

    while not flag: # if the above flag is not triggred then the file isnt read 
        if storage[i]== ".end\n": #exit if the circuit ends
            flag=True
        else:
            data=storage[i].split()
            component_name=data[0]
            if component_name[0] not in valid_components:
                raise ValueError('Only V, I, R elements are permitted')
            
            for p in data:
                if p[0] == "#":
                    data.remove(p)

            if component_name[0] == "R":
                if len(data) != 4:
                    raise ValueError('Malformed circuit file')
            if component_name[0] == "V" or component_name[0] == "I":
                if len(data) != 5:
                    raise ValueError('Malformed circuit file')            

            node1=data[1]
            node2=data[2]
            branch=(node1,node2)

            # in case the 4th element is a string dc or ac
            value = data[3]
            try:
                value = float(value)  # Convert to float directly if possible
            except ValueError:
                if 'e' in value:  # Check for scientific notation like '1e3'
                    value = float(value)
                else:
                    value = float(data[4])

            if node1 not in ascending_list_of_nodes:
                ascending_list_of_nodes.append(node1)
            if node2 not in ascending_list_of_nodes:
                ascending_list_of_nodes.append(node2)

            # we will now populate the node_connection dictionary 
            if node1 in node_connections:
                node_connections[node1].append((node2,component_name)) # adding node 2 to the list of nodes for node 1
            else:
                node_connections[node1]=[(node2,component_name)]
            
            if node2 in node_connections:
                node_connections[node2].append((node1,component_name)) # adding node 1 to the list of nodes for node 2
            else:
                node_connections[node2]=[(node1,component_name)]

            #populating branch components
            #types of components = R V I 
            branch_components[component_name]=[component_name[0],branch,value]
            if component_name[0]=="V":
                aux_eqns+=1 # getting no of voltage sources to use as auxilarry equations
                aux_list.append(component_name)
            # structure of list = component type, connected branch , value ,
            # None to store the current through the voltage source or potential accross a current source
        i+=1

    '''we will check for voltage sources connected in parallel'''
    if aux_eqns > 1:
            for i in aux_list:
                branch=branch_components[i][1] # this will give we the nodes this voltage source is connected to
                for k in aux_list:
                    if k != i:
                        node1,node2=branch_components[k][1]
                        if (node1,node2) == branch:
                            raise ValueError('Circuit error: no solution')
                        if (node2,node1) == branch:
                            raise ValueError('Circuit error: no solution')           



    # setting up equations to solve for unknowns
    # no of unknows is no of nodes + no of voltage sources -1
    no_of_unknowns=len(node_connections)+aux_eqns-1 
    
    # voltage at each node is unknown and ground node is known  
    # and we have aux_eqns no of auxiliary equations
    # now a matrix will be created with unknown node voltages arranged in the order of ascending_list_of_nodes

    coefficient_matrix=np.zeros((no_of_unknowns,no_of_unknowns))
    constant_matrix=np.zeros(no_of_unknowns)          

    #populating the matrices
    ascending_list_of_nodes.remove("GND") #remode the ground node from the list of unknowns
    unknown_list=ascending_list_of_nodes+aux_list    
    if len(unknown_list) != no_of_unknowns:
        raise ValueError('Circuit error: no solution')
    
    count_of_equations=0    #used as an index
    current_source_flag=False

    for i in ascending_list_of_nodes: # i is the node we are working with
        #writing KCL
        for k in node_connections[i]:
            node,component=k # k=(connected node, component)

            '''here i do not require node as bringing in component attached to each node gives me the connected node'''

            data=branch_components[component] # structure of data ['R', ('1', '2'), 1.0] 

            #here we do (Vnode1-Vnode2)/R (KCL). 
            #If node1 or node2 is ground (it is not in the unknown_list) then we ignore it 

            node1,node2=data[1] # this is the branch where the component is connected
            if node1==i: # else the direction of current is reversed 
                m=1
            else: 
                m=-1

            if data[0]=="R":                
                #If either of the nodes is ground we dont bother adding them to the equations as its cofficient is zero (Vnode1-0)/R
                #m decides the direction of current
                if node1 in unknown_list:
                    coefficient_matrix[count_of_equations][unknown_list.index(node1)]+=   (m*1)/data[2] #we update the values from zero(default)
                if node2 in unknown_list:
                    coefficient_matrix[count_of_equations][unknown_list.index(node2)]+=   (-1*m)/data[2]

            if data[0]=="V":
                #here we have to do KCL with the unknown current throught the Vsourve
                #the unknow current is present in the unknows list and so we can just add its cofficients to the matrix to solve
                if node1 == i:
                    coefficient_matrix[count_of_equations][unknown_list.index(component)]+= 1
                else:
                    coefficient_matrix[count_of_equations][unknown_list.index(component)]+= -1
                
                
            if data[0]=="I": # do same as above for V
                current_source_flag=True 
                constant_matrix[count_of_equations] += -m*data[2] 
                # m decides the direction -m as this constant term goes to the RHS of the equation
        
        
        # if multiple current sources enter a node and nothing leaves that means kcl is violated 
        if not np.any(coefficient_matrix[count_of_equations]): # returns false if the array is all zeros 
            if current_source_flag: #all current sources entering one branch 
                if constant_matrix[count_of_equations] == 0 :# the currents cancel
                    raise ValueError('Circuit error: no solution')
            raise ValueError('Circuit error: no solution') #raise error if the matrix contains a zero row 
        


        constant_matrix[count_of_equations]  +=   0 # all of this 
        count_of_equations+=1 #after completing KCL at this node we populate the next equation
        print(node_connections,"\n\n",branch_components,"\n\nmatrix\n",coefficient_matrix,"\nconstant matrix\n",constant_matrix)
        print()
        
    #writing aux_equations
    for i in aux_list:
        #here we do Vnode1-Vnode2= Vsource
        data=branch_components[i]
        node1,node2=data[1]
        #If either of the nodes is ground we dont bother adding them to the equations as its cofficient is zero (Vnode1-0)=Vsource
        if node1 in unknown_list:
            coefficient_matrix[count_of_equations][unknown_list.index(node1)]  +=   1
        if node2 in unknown_list:
            coefficient_matrix[count_of_equations][unknown_list.index(node2)]  +=   -1

        constant_matrix[count_of_equations]                                     =   data[2]
        count_of_equations+=1
    
    # let us now catch invalid circuits 
    det=np.linalg.det(coefficient_matrix)
    if det == 0 :     # checking the matrix is singular 
        raise ValueError('Circuit error: no solution')
    else:
        X=np.linalg.solve(coefficient_matrix,constant_matrix)   #X has the final solutions
        
        #now a list of node voltages and branch currents needs to be returned
        V=dict() # node voltages
        I=dict() # breanch current
        V["GND"]=0.0 # we had to remove this node earlier

        count_of_equations=0
        for i in range(len(ascending_list_of_nodes)):
            V[ascending_list_of_nodes[i]]=X[count_of_equations]
            count_of_equations+=1
        for i in range(len(aux_list)):
            I[aux_list[i]] = X[count_of_equations]
            count_of_equations+=1

        
        print(node_connections,"\n\n",branch_components,"\n\nmatrix\n",coefficient_matrix,"\nconstant matrix\n",constant_matrix)
        print()
        print(ascending_list_of_nodes,"\n",aux_list)
        for i in range(len(unknown_list)):
            print(unknown_list[i],"=",X[i],)
        print(V)
        print(I)
evalSpice('test_1.ckt')