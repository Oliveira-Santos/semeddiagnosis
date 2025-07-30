document.addEventListener('DOMContentLoaded', function () {
    console.log("search.js carregado com sucesso");

    const bairroSelect = document.getElementById('bairro');

    if (bairroSelect) {
        fetch('/get-bairros/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta da API');
                }
                return response.json();
            })
            .then(data => {
                if (!data.bairros) {
                    throw new Error('Formato de dados inválido');
                }

                data.bairros.forEach(bairro => {
                    const option = document.createElement('option');
                    option.value = bairro.id;
                    option.text = bairro.bairro_distrito;
                    bairroSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Erro ao carregar bairros:", error.message);
            });
    }
});
