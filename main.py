from speckle_automate import (
    execute_automate_function,
)


from model_checker.function import automate_function
from model_checker.inputs import FunctionInputs


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!


    execute_automate_function(automate_function, FunctionInputs)
