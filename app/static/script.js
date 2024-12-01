const analyzeBtn = document.getElementById('analyze-btn');
const urlInput = document.getElementById('url-input');
const resultTab = document.querySelector('.result-tab');

analyzeBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();

    if (!url) {
        alert('Пожалуйста, введите ссылку!');
        return;
    }

    analyzeBtn.textContent = 'Анализ...';
    analyzeBtn.disabled = true;

    try {
        console.log(encodeURIComponent(url))
        const response = await fetch('http://127.0.0.1:8000/check/', {
            method: 'POST',
            headers: {
                'content-type': 'application/json',
            },
            body: `{"url": "${encodeURIComponent(url)}"}
            `, 
        });

        if (!response.ok) {
            throw new Error('Сервер вернул ошибку: ' + response.statusText);
        }

        const result = await response.json();

        // Обновление результатов
        document.getElementById('result-title').textContent = `РЕЗУЛЬТАТ ПРОВЕРКИ: ${encodeURIComponent(url)}`;
        document.getElementById('rating').textContent = result.rating;
        const issuesList = document.getElementById('issues-list');
        issuesList.innerHTML = '';
        result.issues.forEach((issue) => {
            const li = document.createElement('li');
            li.textContent = issue;
            issuesList.appendChild(li);
        });

        document.getElementById('report-link').href = result.reportLink;

        resultTab.classList.remove('hidden');

    } catch (error) {
        console.error('Ошибка при анализе:', error);
    } finally {
        analyzeBtn.textContent = 'Анализировать';
        analyzeBtn.disabled = false;
    }
});
