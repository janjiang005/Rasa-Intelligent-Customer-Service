function a() {
    console.log(1);
}
function b() {
    var ps = new Promise(function(success, fail) {
        success();
    });

    ps.then(function() {
        console.log("success");
    }).then(function() {
        console.log("success2");
    });
}

function c() {
    console.log("kaishi");
    b();
    a();
}
console.log(1);

c();
