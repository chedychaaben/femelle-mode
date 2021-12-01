var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var articleId = this.dataset.article
        var action = this.dataset.action 
        
        
        updateOrder(articleId, action)
    })
}

function updateOrder(articleId, action){
    var url = '/update_item/'
    fetch(url, {
        method :'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'articleId': articleId, 'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then(() =>{
        location.reload()
    })
}