// Initialize all Materialize components
M.AutoInit();

// Open the modal when user is redirected to login
let params = window.location.search;
if (params.includes('next')) {
    let elem = document.querySelector('.modal');
    let instance = M.Modal.getInstance(elem);
    instance.open();
}