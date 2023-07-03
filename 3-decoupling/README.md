# DAY 3: decoupling

Download the provided code for the challenge.  
Challenge:

1. Identify the current code structure and its limitations:

- Analyze the BankService class in bank.py.
- Understand the high coupling between the BankService class, payment service, and account types.
- Identify areas of code duplication.

2. Plan the refactoring strategy:

- Determine the desired level of decoupling between banking and payment operations.
- Decide on an approach to reduce coupling and eliminate code duplication.
- Consider introducing new classes or replacing existing classes with functions, as needed.

3. Refactor the code:

- Modify the BankService class and related components to reduce coupling.
- Extract common code and eliminate duplications.
- Consider creating separate classes or functions for banking and payment operations.

4. Test the refactored code:

- Ensure that banking operations are decoupled from payment operations as intended.
- Verify that the refactored code retains the desired functionality
- Conduct thorough testing to validate the correctness of the changes.

5. Evaluate the effectiveness of the refactoring:

- Assess the impact of the refactoring on code structure, maintainability, and readability.
- Determine if the desired level of decoupling and code reuse has been achieved.
- Consider soliciting feedback from peers or conducting code reviews to gather different perspectives.

6. Document the changes:

- Update relevant documentation or comments to reflect the refactored code.
- Provide clear explanations of the changes made and their benefits.
- Document any new classes or functions introduced during the refactoring process.

7. Review and iterate:

- Review the refactored code and documentation for accuracy and completeness.
- Iterate on the refactoring, if necessary, to address any overlooked issues or further enhance the codebase.
