document.addEventListener('DOMContentLoaded', function() {
    const translateBtn = document.getElementById('translate-btn');
    const sourceText = document.getElementById('source-text');
    const sourceLang = document.getElementById('source-lang');
    const targetLang = document.getElementById('target-lang');
    const translatedText = document.getElementById('translated-text');

    translateBtn.addEventListener('click', function() {
        const text = sourceText.value;
        const source = sourceLang.value;
        const target = targetLang.value;

        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                source_lang: source,
                target_lang: target
            })
        })
        .then(response => response.json())
        .then(data => {
            translatedText.innerText = data.translated_text;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});