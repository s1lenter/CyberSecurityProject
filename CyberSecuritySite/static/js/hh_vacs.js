function toggleContent() {
    const content = document.getElementById('additional-content');
    const button = document.getElementById('toggle-button');

    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.textContent = 'Скрыть детали';
    } else {
        content.style.display = 'none';
        button.textContent = 'Показать детали';
    }
}