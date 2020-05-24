$(document).ready(function () {
    var ingredientNum = 1;

    $("#ingredient").on("click", ".ibtnIngredientAdd",function(event) { 
    var newRow = $('<div class="form-row" id="ingredient-row-'+ ingredientNum + '">');
    var cols = "";

    cols += '<div class="form-group col-sm-2"><div class="form-group required"><input class="form-control" id="ingredient-' + ingredientNum + '-quantity" list="quantity_datalist" name="ingredient-' + ingredientNum + '-quantity" placeholder="Quantity" required="" type="text" value=""></div></div>';
    cols += '<div class="form-group col-sm-2"><div class="form-group required"><input class="form-control" id="ingredient-' + ingredientNum + '-unit" list="unit_datalist" name="ingredient-' + ingredientNum + '-unit" placeholder="Unit" required="" type="text" value=""></div></div>';
    cols += '<div class="form-group col-sm-2"><div class="form-group required"><input class="form-control" id="ingredient-' + ingredientNum + '-ingredient" list="ingredient_datalist" name="ingredient-' + ingredientNum + '-ingredient" placeholder="Ingredient" required="" type="text" value=""></div></div>';
    cols += '<div class="form-group col-sm-1"><div class="form-group"><input class="form-control ibtnIngredientAdd btn btn-md btn-success btn-sm" required="" type="button" value="Add"></div></div>';
    cols += '<div class="form-group col-sm-1"><div class="form-group"><input class="form-control ibtnIngredientDelete btn btn-md btn-danger btn-sm" required="" type="button" value="Delete"></div></div>';

    newRow.append(cols);
    $("#ingredient").append(newRow); 
    ingredientNum++; 
    });

    $("#ingredient").on("click", ".ibtnIngredientDelete", function (event) {
        var $baseRow = document.getElementById("ingredient-row-0");
        var $deleteElement = $(this).closest('div.form-row');
        if ($deleteElement[0].id != $baseRow.id && ingredientNum >= 1) {
            $deleteElement.remove();
            ingredientNum -= 1
        }
    });

    var stepNum = 1;

    $("#step").on("click", ".ibtnStepAdd",function(event) { 
    var newRow = $('<div class="form-row" id="step-row-'+ stepNum + '">');
    var cols = "";

    cols += '<div class="form-group col-sm-1"><div class="form-group  required"><input class="form-control" id="step-' + stepNum + '-step_number" name="step-' + stepNum + '-step_number" readonly="" required="" type="text" value="' + (stepNum+1)  + '"></div></div>';
    cols += '<div class="form-group col-sm-5"><div class="form-group required"><input class="form-control" id="step-' + stepNum + '-step" name="step-' + stepNum + '-step" placeholder="Step" required="" type="text" value=""></div></div>';
    cols += '<div class="form-group col-sm-1"><div class="form-group"><input class="form-control ibtnStepAdd btn btn-md btn-success btn-sm" required="" type="button" value="Add"></div></div>';
    cols += '<div class="form-group col-sm-1"><div class="form-group"><input class="form-control ibtnStepDelete btn btn-md btn-danger btn-sm" required="" type="button" value="Delete"></div></div>';

    newRow.append(cols);
    $("#step").append(newRow); 
    stepNum++; 
    });

    $("#step").on("click", ".ibtnStepDelete", function (event) {
        var $baseRow = document.getElementById("step-row-0");
        var $deleteElement = $(this).closest('div.form-row');
        if ($deleteElement[0].id != $baseRow.id && stepNum >= 1) {
            $deleteElement.remove();
            stepNum -= 1
        }
    });
});