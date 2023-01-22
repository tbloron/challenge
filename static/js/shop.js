function createProduct() {
    $.ajax({
        type: "POST",
        url: "/products/",
        data: {"name": $("#name").val(), "price": $("#price").val()},
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    });
};

function deleteProduct(id) {
    $.ajax({
        type: "DELETE",
        url: "/products/" + id,
        success: function() {
            window.location.replace("/products")
        },
        error: function(xhr, status, error) {
            if (xhr.status === 404) {
                alert(error);
            } else {
                var err = JSON.parse(xhr.responseText);
                alert(err.message);
            }
        }
    });
};

function updateProduct(id) {
    $.ajax( {
        type: "PUT",
        url : "/products/" + id,
        contentType: 'application/json',
        data: JSON.stringify({"name": $("#productName").val(), "price": $("#productPrice").val()}),
        success: function (response) {
            window.location =  "/products/";
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    });
}

function createOrder() {
    $.ajax({
        type: "POST",
        url: "/sells/",
        data: {"customer": $("#orderCustomer").val()},
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    });
};

function createOrderItem(id) {
    $.ajax({
        type: "POST",
        url: "/sells/" + id,
        data: {"product_name": $("#itemProduct").val(), "quantity": $("#itemQuantity").val()},
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    });
}

function deleteOrderItem(order, item) {
    $.ajax({
        type: "DELETE",
        url: "/sells/" + order + "/items/" + item,
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    })
}

function incrementOrderItem(order, item) {
    $.ajax({
        type: "POST",
        url: "/sells/" + order + "/items/" + item + "/increment",
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    })
}

function decrementOrderItem(order, item) {
    $.ajax({
        type: "POST",
        url: "/sells/" + order + "/items/" + item + "/decrement",
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    })
}

function validateOrder(id) {
    $.ajax({
        type: "POST",
        url: "/sells/" + id + "/validate",
        success: function () {
            window.location.reload();
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    })
}

function addProductToOrder(id) {
    $.ajax({
        type: "POST",
        url: "/products/" + id + "/add_to_order",
        success: function(response) {
            alert(response.product + " added in your basket");
        }
    })
}

function getBasket() {
    $.ajax({
        type: "GET",
        url: "/sells/basket/",
        success: function (response) {
            window.location.replace("/sells/" + response.pk)
        },
        error: function(xhr, status, error) {
            var err = JSON.parse(xhr.responseText);
            alert(err.message);
        }
    })
}