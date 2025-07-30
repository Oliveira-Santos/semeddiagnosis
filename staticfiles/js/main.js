// Função para aplicar máscara no CPF
$(document).ready(function () {
    if (typeof $.fn.mask !== 'undefined') {
        $('#cpfInput, #cpf').mask('000.000.000-00');
    }

    // Verificação de CPF (Cadastro Modal)
    $('#verificarCpfBtn').on('click', function () {
        const cpf = $('#cpf').val();
        const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        if (!cpf) {
            alert("Por favor, digite um CPF válido.");
            return;
        }

        $.ajax({
            url: '/verificar-cpf/',
            method: 'POST',
            data: {
                'cpf': cpf,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (response) {
                if (response.status === 'existe') {
                    alert("Este CPF já está cadastrado.");
                } else if (response.status === 'nao_existe') {
                    $('#cpf').val(cpf).prop('readonly', true);
                    $('#cadastroModal').modal('show');
                    $('#verificarCpfModal').modal('hide');
                } else {
                    alert("Erro inesperado ao verificar o CPF.");
                }
            },
            error: function () {
                alert("Erro ao verificar o CPF.");
            }
        });
    });

    // CPF Admin (Modal separado)
    $('#verifyCpfBtn').on('click', function () {
        const cpf = $('#cpfInput').val();
        const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            url: '/verificar-cpf/',
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: {
                'cpf': cpf
            },
            success: function (data) {
                if (data.status === 'success') {
                    $('#cpfModal').modal('hide');
                    window.location.href = data.redirect_url;
                } else {
                    $('#cpfErrorMessage').text(data.message || 'CPF não autorizado.');
                }
            },
            error: function () {
                $('#cpfErrorMessage').text('Erro ao verificar o CPF.');
            }
        });
    });

    // Limpar modal CPF Admin
    $('#cpfModal').on('hidden.bs.modal', function () {
        $('#cpfForm')[0].reset();
        $('#cpfErrorMessage').text('');
    });

    $('#cancelBtn').on('click', function () {
        $('#cpfModal').modal('hide');
    });

    console.log("main.js carregado com sucesso");
});
