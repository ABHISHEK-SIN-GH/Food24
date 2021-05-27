
$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1.7,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 2.5,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var qu = this.parentNode.children[2]
    // console.log(id)
    $.ajax({ type:"GET", url:"/plus-cart", data:{prod_id:id}, 
    success:function(data){
        qu.innerText = data.quantity
        document.getElementById("amount").innerText = data.Amt
        document.getElementById("total").innerText = data.totalAmt
    }

})
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var qu = this.parentNode.children[2]
    // console.log(id)
    $.ajax({ type:"GET", url:"/minus-cart", data:{prod_id:id}, 
    success:function(data){
        qu.innerText = data.quantity
        document.getElementById("amount").innerText = data.Amt
        document.getElementById("total").innerText = data.totalAmt
    } 
})
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var qu = this
    // console.log(id)
    $.ajax({ type:"GET", url:"/remove-cart", data:{prod_id:id}, 
    success:function(data){
        document.getElementById("amount").innerText = data.Amt
        document.getElementById("total").innerText = data.totalAmt
        qu.parentNode.parentNode.parentNode.parentNode.remove()
    } 
})
})








