document.addEventListener('DOMContentLoaded', function() {
    getVisitCount();
});

const productionApiUrl = 'https://getwebcounter.azurewebsites.net/api/counter';
const localApiUrl = 'http://localhost:7071/api/counter';

function getVisitCount() {
    fetch(productionApiUrl, {
        method: "POST",
        headers: { Accept: "application/json" }
    }).then(response => {
        return response.json();
    }).then(response => {
        console.log("Website called function API.");
        const count = response.count;
        document.getElementById("visitor-count").innerText = count ? count.toLocaleString() : "--";
    }).catch(function(error) {
        console.log(error);
        document.getElementById("visitor-count").innerText = "--";
    });
};
