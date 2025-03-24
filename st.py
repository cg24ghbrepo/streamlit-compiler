import streamlit as st
from flask import Flask, request, jsonify
import sys
import io
import numpy as np
import scipy.stats as stats

# Initialize Flask app
app = Flask(__name__)

# Function to execute code and check standard test cases
def execute_code(code):
    # Prepare to capture output
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    result = io.StringIO()
    sys.stdout = result
    sys.stderr = result

    # Standard test case for normal distribution (mean=0, std=1)
    test_x = np.array([0, 1, 2])
    expected_output = stats.norm.pdf(test_x, loc=0, scale=1)

    try:
        # Execute the code sent from WordPress
        exec(code)

        # Example: check the output against the expected result for normal distribution
        if 'compute_normal_distribution' in globals():
            output = compute_normal_distribution(0, 1, test_x)
            pass_test = np.allclose(output, expected_output)

            if pass_test:
                return "Test passed: The normal distribution function works correctly!"
            else:
                return f"Test failed. Output: {output}, Expected: {expected_output}"
        else:
            return "Error: Function 'compute_normal_distribution' not defined."

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# Endpoint to handle code execution
@app.route('/execute', methods=['POST'])
def handle_code_execution():
    # Get the code from the request
    code = request.json.get('code')

    if not code:
        return jsonify({"error": "No code provided!"}), 400

    # Execute the code and check against the test cases
    result = execute_code(code)

    return jsonify({"result": result})

if __name__ == '__main__':
    # Run Flask server
    app.run(host='0.0.0.0', port=5000)
