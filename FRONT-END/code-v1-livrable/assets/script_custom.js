 
 
 
 
 // Fonction pour charger le nombre total d'avis
 fetch('http://127.0.0.1:8000/total_reviews')
 .then(response => response.json())
 .then(data => {
   document.getElementById('totalReviews').innerText = data.total_reviews;
 })
 .catch(error => console.error('Erreur:', error));





     // Fonction pour charger la distribution des scores
     fetch('http://127.0.0.1:8000/score_distribution')
     .then(response => response.json())
     .then(data => {
       const labels = data.map(item => `${item.score} Étoile`);
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





        // Fonction pour charger le taux d'avis positifs vs négatifs
    fetch('http://127.0.0.1:8000/sentiment_ratio')
    .then(response => response.json())
    .then(data => {
      const labels = Object.keys(data);
      const values = Object.values(data);
      
      new Chart(document.getElementById('sentimentRatioChart'), {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: values,
            backgroundColor: [
              'rgba(75, 192, 192, 0.6)', // Positive
              'rgba(255, 99, 132, 0.6)', // Negative
              'rgba(201, 203, 207, 0.6)'  // Neutral
            ],
            borderColor: [
              'rgba(75, 192, 192, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(201, 203, 207, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {}
      });
    })
    .catch(error => console.error('Erreur:', error));





        // Fonction pour charger la note moyenne par période
        fetch('http://127.0.0.1:8000/average_score_over_time?freq=M')
        .then(response => response.json())
        .then(data => {
          const labels = data.map(item => item.at.slice(0, 7)); // Format YYYY-MM
          const values = data.map(item => parseFloat(item.average_score.toFixed(2)));
          
          new Chart(document.getElementById('averageScoreOverTimeChart'), {
            type: 'line',
            data: {
              labels: labels,
              datasets: [{
                label: 'Note Moyenne',
                data: values,
                fill: true,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                tension: 0.1
              }]
            },
            options: {
              scales: {
                y: { beginAtZero: true, max: 5 }
              }
            }
          });
        })
        .catch(error => console.error('Erreur:', error));



        
            // Fonction pour charger les avis par version de l'application
    fetch('http://127.0.0.1:8000/reviews_by_version')
    .then(response => response.json())
    .then(data => {
      const labels = data.map(item => item.reviewCreatedVersion);
      const reviewCounts = data.map(item => item.review_count);
      const averageScores = data.map(item => parseFloat(item.average_score.toFixed(2)));
      
      new Chart(document.getElementById('reviewsByVersionChart'), {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Nombre d\'Avis',
              data: reviewCounts,
              backgroundColor: 'rgba(255, 206, 86, 0.6)',
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 1
            },
            {
              label: 'Note Moyenne',
              data: averageScores,
              type: 'line',
              fill: false,
              borderColor: 'rgba(75, 192, 192, 1)',
              yAxisID: 'y-axis-2'
            }
          ]
        },
        options: {
          scales: {
            y: { 
              beginAtZero: true,
              position: 'left',
              title: {
                display: true,
                text: 'Nombre d\'Avis'
              }
            },
            'y-axis-2': {
              beginAtZero: true,
              position: 'right',
              title: {
                display: true,
                text: 'Note Moyenne'
              },
              grid: { drawOnChartArea: false }
            }
          }
        }
      });
    })
    .catch(error => console.error('Erreur:', error));






       // Fonction pour charger la distribution des "Thumbs Up"
       fetch('http://127.0.0.1:8000/thumbs_up_distribution')
       .then(response => response.json())
       .then(data => {
         const labels = data.map(item => item.thumbsUpCount);
         const values = data.map(item => item.count);
         
         new Chart(document.getElementById('thumbsUpDistributionChart'), {
           type: 'bar',
           data: {
             labels: labels,
             datasets: [{
               label: 'Nombre d\'Avis',
               data: values,
               backgroundColor: 'rgba(255, 159, 64, 0.6)',
               borderColor: 'rgba(255, 159, 64, 1)',
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




           // Fonction pour charger le sentiment moyen combiné
    fetch('http://127.0.0.1:8000/combined_sentiment_average')
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById('combinedSentimentAverageChart').getContext('2d');
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Positive', 'Négative'],
          datasets: [{
            data: [data.average_combined_score, 5 - data.average_combined_score],
            backgroundColor: [
              'rgba(75, 192, 192, 0.6)',
              'rgba(255, 99, 132, 0.6)'
            ],
            borderColor: [
              'rgba(75, 192, 192, 1)',
              'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return context.label + ': ' + context.parsed.toFixed(2);
                }
              }
            }
          }
        }
      });
    })
    .catch(error => console.error('Erreur:', error));



    
    // Fonction pour charger la fréquence des avis par heure de la journée
    fetch('http://127.0.0.1:8000/review_frequency_by_hour')
      .then(response => response.json())
      .then(data => {
        const labels = data.map(item => `${item.hour}:00`);
        const values = data.map(item => item.review_count);
        
        new Chart(document.getElementById('reviewFrequencyByHourChart'), {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Nombre d\'Avis',
              data: values,
              backgroundColor: 'rgba(255, 99, 132, 0.6)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: { beginAtZero: true, precision: 0 },
              x: { title: { display: true, text: 'Heure de la Journée' } }
            }
          }
        });
      })
      .catch(error => console.error('Erreur:', error));





          // Fonction pour charger les tendances de sentiment par version de l'application
    fetch('http://127.0.0.1:8000/sentiment_trends_by_version?freq=M')
    .then(response => response.json())
    .then(data => {
      // Filtrer les données par sentiment
      const positiveData = data.filter(item => item.sentiment === 'positive');
      const negativeData = data.filter(item => item.sentiment === 'negative');
      const neutralData = data.filter(item => item.sentiment === 'neutral');
      
      // Extraire les labels (versions)
      const versions = [...new Set(data.map(item => item.reviewCreatedVersion))];
      
      // Organiser les données par version
      const sentimentCounts = {
        positive: [],
        negative: [],
        neutral: []
      };
      
      versions.forEach(version => {
        const pos = positiveData.filter(item => item.reviewCreatedVersion === version).reduce((sum, item) => sum + item.count, 0);
        const neg = negativeData.filter(item => item.reviewCreatedVersion === version).reduce((sum, item) => sum + item.count, 0);
        const neu = neutralData.filter(item => item.reviewCreatedVersion === version).reduce((sum, item) => sum + item.count, 0);
        
        sentimentCounts.positive.push(pos);
        sentimentCounts.negative.push(neg);
        sentimentCounts.neutral.push(neu);
      });
      
      new Chart(document.getElementById('sentimentTrendsByVersionChart'), {
        type: 'bar',
        data: {
          labels: versions,
          datasets: [
            {
              label: 'Positive',
              data: sentimentCounts.positive,
              backgroundColor: 'rgba(75, 192, 192, 0.6)'
            },
            {
              label: 'Negative',
              data: sentimentCounts.negative,
              backgroundColor: 'rgba(255, 99, 132, 0.6)'
            },
            {
              label: 'Neutral',
              data: sentimentCounts.neutral,
              backgroundColor: 'rgba(201, 203, 207, 0.6)'
            }
          ]
        },
        options: {
          scales: {
            x: { stacked: true },
            y: { stacked: true, beginAtZero: true }
          }
        }
      });
    })
    .catch(error => console.error('Erreur:', error));