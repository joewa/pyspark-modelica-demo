import pandas as pd
import TestBouncingBall


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    parameters_var_df = pd.DataFrame(columns=['run_key', 'modifiers'], data=[
        ['r1', ['e=0.7']],
        ['r2', ['e=0.5']],
        ['r3', ['e=0.9']],
    ])
    result_pdf = TestBouncingBall.run_bouncingball_pandas(parameters_var_df)
    print(result_pdf)
