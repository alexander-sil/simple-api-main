async function transliterate(text) {
    const response = await fetch('/арі', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: text })
    });
    const result = await response.json();
    return result.data;
}

async function saveTranslation(originalText, transliteratedText) {
    await fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ original: originalText, transliterated: transliteratedText })
    });
}

async function getHistory() {
    const historyCount = document.getElementById('historyCount').value;
    if (!Number.isInteger(+historyCount) || +historyCount <= 0) {
        alert("Введите корректное положительное число");
        return;
    }
    const response = await fetch(`/history?n=${historyCount}`);
    const result = await response.json();

    const historyOutput = document.getElementById('historyOutput');
    historyOutput.innerHTML = result.data.map(item => `${item.original} -> ${item.transliterated}`).join('<br>');
}

function handleInputChange(event) {
    const inputText = event.target.value;

    const outputField = document.getElementById('output');
    if (event.target.id === 'input1') {
        transliterate(inputText).then(transliteratedText => {
            outputField.value = transliteratedText;
        });
    } else {
        outputField.value = '';
    }
}

async function handleSave() {
    const inputText = document.getElementById('input1').value;
    const outputText = document.getElementById('output').value;
    await saveTranslation(inputText, outputText);
    alert('Сохранено в базу данных');
}
