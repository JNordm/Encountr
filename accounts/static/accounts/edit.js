var is_first_job = document.querySelector('#is_first_job');
var last_company = document.getElementById("last_company");

console.log(is_first_job)

is_first_job.addEventListener('change', function(){
	if(is_first_job.checked){
		last_company.style.display = "none";
	} else{
		last_company.style.display = "";
	}
})