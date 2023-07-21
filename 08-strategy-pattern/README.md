# DAY 8: Strategy Pattern

Task 1: Understand the current payment processing implementation

- Review the existing codebase and understand how the payment processing is currently implemented within the ShoppingCart class.
- Identify the tight coupling between the ShoppingCart and the specific payment methods (credit card, PayPal, Apple Pay).

Task 2: Design the Strategy pattern approach

- Plan a new design for the payment processing system using the Strategy pattern.
- Identify the set of related algorithms (payment strategies) that need to be encapsulated in separate classes.
- Determine how the ShoppingCart class can interact with the payment strategies without knowing the implementation details.

Task 3: Create payment strategy classes

- Implement separate classes for each payment strategy (credit card, PayPal, Apple Pay).
- Ensure that each payment strategy class provides a consistent interface for the ShoppingCart to interact with.

Task 4: Refactor the ShoppingCart class

- Modify the existing code within the ShoppingCart class to utilize the payment strategy classes.
- Remove the direct implementation details of each payment method from the ShoppingCart class.

Task 5: Make the payment strategy interchangeable

- Ensure that the ShoppingCart class can dynamically switch between different payment strategies at runtime.
- Implement the necessary changes to allow the customer to choose their preferred payment method.

Task 6: Test the refactored code

- Run tests to ensure that the refactored code correctly uses the Strategy pattern for payment processing.
- Verify that the ShoppingCart class can handle different payment strategies seamlessly.

Task 7: Document the changes made

- Document the areas of code that were modified to implement the Strategy pattern for payment processing.
- Explain how the design patterns and changes made reduce coupling between the ShoppingCart and payment methods.
- Provide instructions on how to add new payment strategies if required.
