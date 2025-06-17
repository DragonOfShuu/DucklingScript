from enum import Enum

class EnvExtendType(Enum):
    NORMAL = "normal"
    """
    Normal environment extension type, used for most cases 
    where the environment is extended without any special conditions.

    User Variables are still accessible, from the previous environment,
    but new variables are not carried over to the previous environment
    (unless they are system variables)
    """
    PARALLEL = "parallel"
    """
    Parallel environment extension type, used for cases where the environment
    is extended to run in parallel with the previous environment.

    User variables are accessible, and creating new variables will
    add the variables to the previous environment as well.
    """
    HARD = "hard"
    """
    Hard environment extension type, used for cases where the environment
    is extended with limitations.

    User variables are not accessible, and creating new variables will
    not add the variables to the previous environment.

    The only connections to the previous environment are system variables,
    the project environment, and the output environment.
    
    This is used for cases where the environment is extended to run in a
    completely isolated environment, such as in a different file.
    """