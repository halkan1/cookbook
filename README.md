# Cookbook/Meal Planner/Shopping Assistant

## Goals

* A fully fledged recipe database with little to no repeated data in the database
* Ability to create a weekly menu from recipes and calculate a summerized shopping list for ingredients in chosen recipes as well as allowing addition of items outside of those recipes.
* Creating a route thorugh the store based on ingredient classification (canned goods, dairy, etc) and sorting the shopping list by that.

## ToDos

- [ ] Clean up current code.
- [ ] Fix Edit Recipe
- [ ] Restructure functions in Forms and Models.
- [ ] Implement ingredients and steps into recipe form.
- [ ] Implement ingredient, measurement, quantity, tag, type views.
- [ ] Investigate support for float values in quantity table. Date Type could be float, double or decimal
- [ ] Implement blueprints (recipes, menues, user and weekly menu/shopping list could probably be different modules).
- [ ] Change URLs (/recipe/add, /recipe/edit/<recipe>, etc would look better).
- [ ] Build function to accept underscore instead of space but convert it when querying database.
- [ ] More UnitTesting.
- [ ] Update Database schema xml to represent the current schema.
- [ ] Change names for Measurment* tables to Ingredient*
- [ ] Implement the use of Errors.
- [ ] Improve HTML code.
- [ ] Style the views.
- [ ] Remove uneccessary user profile parts.
- [ ] Fix titles (either static or variable not both)
- [ ] Remove Flask-Bootstrap and include as a static asset instead
- [ ] Instead of relying on existing Ingredient sets allow user to add a new set if it does not exists via a modal
- [ ] Move add recipe Javascript to the relevant template
- [ ] Improve layout of index with cards for each recipe shown and pagination
- [ ] Improve Add and Delete for Ingredients and Steps in forms
- [ ] Create a seperate view or Droplist from navbar to add smaller things like ingredients and units...
- [ ] Allow access to index and individual recipes without being logged in.
- [ ] Make login a dropdown from the user icon at the top right instead.
