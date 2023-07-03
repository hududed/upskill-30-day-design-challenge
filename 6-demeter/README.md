# DAY 6: Demeter

Task 1: Analyze the codebase

- Review the provided codebase and understand its structure and functionality.
- Identify instances where objects are violating the Law of Demeter by directly interacting with the attributes or methods of unrelated objects.

Task 2: Identify violations of the Law of Demeter

- Identify the specific code segments or instances where violations of the Law of Demeter occur.
- Determine which objects are directly interacting with the attributes or methods of unrelated objects.

Task 3: Refactor the code to remove violations

- Modify the existing code to adhere to the Law of Demeter.
- Identify the primary purpose of each object and restrict its interactions to its immediate friends only.
- Encapsulate and delegate functionality where necessary to avoid direct interactions with unrelated objects.

Task 4: Test the refactored code

- Verify that the refactored code produces the same results as the original code.
- Conduct thorough testing to ensure the changes did not introduce any new bugs or issues.
- Validate that the refactored code follows the Law of Demeter and maintains appropriate object interactions.

Task 5: Document the changes made

- Document the areas of code where violations of the Law of Demeter were identified and the corresponding refactorings made.
- Explain the new design decisions and patterns used to remove the violations and improve code maintainability.
- Describe how object interactions were restricted to immediate friends and provide examples of the updated code.
