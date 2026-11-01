let password=document.getElementById('password');
let btn=document.getElementById('toggle');

btn.addEventListener('click',function(){
    
    if (password.type=='password'){
        password.type='text';
        btn.textContent='Hide';
    }
    else{
        password.type='password';
        btn.textContent='Show'
    }
});

// alert('success')