/* static/js/scripts.js */

// Fonction pour charger les graphiques du total des avis
function loadTotalReviews() {
    fetch('http://127.0.0.1:8000/total_reviews')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalReviews').innerText = data.total_reviews;
        })
        .catch(error => console.error('Erreur:', error));
}

// Fonction pour charger la distribution des scores
function loadScoreDistribution() {
    fetch('http://127.0.0.1:8000/score_distribution')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => `Étoile ${item.score}`);
            const values = data.map(item => item.count);

            new Chart(document.getElementById('scoreDistributionChart'), {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Nombre d\'Avis',
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true, precision: 0 }
                    }
                }
            });
        })
        .catch(error => console.error('Erreur:', error));
}

// Fonction pour charger les autres KPI et graphiques selon les catégories
document.addEventListener('DOMContentLoaded', () => {
    loadTotalReviews();
    loadScoreDistribution();
    // Ajoutez ici d'autres fonctions de chargement de KPI
});
