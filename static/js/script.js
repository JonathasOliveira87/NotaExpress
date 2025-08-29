// Função para menu do painel do usuário
function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.style.display = (dropdownContent.style.display === "block") ? "none" : "block";
}


document.addEventListener("DOMContentLoaded", function () {
    // Esconde as mensagens após 5 segundos
    setTimeout(function () {
        $('.messages').fadeOut('slow');
    }, 5000);  // 5000 milissegundos (5 segundos)
});


// Função para calcular o total de horas ao criar ordem
function formatarNumero(numero) {
    return numero < 10 ? '0' + numero : numero;
}


function calcularTotalHoras() {
    var inicio = new Date(document.getElementById('hinicio').value);
    var fim = new Date(document.getElementById('hfim').value);

    // Verificar se a data de fim é menor que a data de início
    if (fim < inicio) {
        document.getElementById('totalHoras').innerText = 'ERRO (Hora Fim)';
    } else {
        var diferencaEmMilissegundos = fim - inicio;
        var horas = Math.floor(diferencaEmMilissegundos / (1000 * 60 * 60));
        var minutos = Math.floor((diferencaEmMilissegundos % (1000 * 60 * 60)) / (1000 * 60));

        var totalHorasString = formatarNumero(horas) + ':' + formatarNumero(minutos) + 'hs';
        document.getElementById('totalHoras').innerText = totalHorasString;

        // Atualizar o valor do campo oculto para total de horas
        document.getElementById('totalHorasInput').value = totalHorasString;
    }
}

document.getElementById('hinicio').addEventListener('change', calcularTotalHoras);
document.getElementById('hfim').addEventListener('change', calcularTotalHoras);


// Criar o JSON dos itens requisitados 
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar que o formulário seja submetido

        // Capturar os valores dos itens requisitados da tabela
        const itensTable = document.querySelector('#itensTable tbody');
        const itensRows = itensTable.querySelectorAll('tr');
        const itensRequisitados = [];

        itensRows.forEach(function(row) {
            const nome = row.cells[0].textContent;
            const quantidade = row.cells[1].textContent;
            const preco = row.cells[2].textContent;

            // Adicionar os valores ao array de itens
            itensRequisitados.push({
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco
            });
        });

        // Converter o array de itens em JSON
        const itensRequisitadosJSON = JSON.stringify(itensRequisitados);

        // Atualizar o valor do campo oculto para itens requisitados
        document.getElementById('itensRequisitadosInput').value = itensRequisitadosJSON;

        // Enviar o formulário
        this.submit();
    });
});

// Função para exibir valor monetário BR
function formatarMoeda(input) {
    // Obtém o valor do campo de preço
    var valor = input.value;

    // Remove todos os caracteres não numéricos, exceto ponto e vírgula
    valor = valor.replace(/[^\d.,]/g, '');

    // Substitui vírgulas por pontos para garantir a interpretação correta como número decimal
    valor = valor.replace(',', '.');


    // Converte o valor para número decimal
    var numeroDecimal = parseFloat(valor);

    // Formata o número para moeda brasileira
    var valorFormatado = numeroDecimal.toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

    // Atualiza o valor no campo de preço
    input.value = valorFormatado;
}

// Função para atualizar a foto ao cadastrar produto
function previewImage() {
    var input = document.getElementById('update_photo');
    var preview = document.getElementById('produto-photo-preview');

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
        }

        reader.readAsDataURL(input.files[0]);
    }
}
