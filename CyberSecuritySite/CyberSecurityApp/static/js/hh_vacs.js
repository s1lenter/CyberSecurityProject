function toggleContent(contentId) {
    const content = document.getElementById(contentId);
    const button = document.getElementById('toggle-button-' + contentId.split('-').pop());

    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.textContent = 'Скрыть описание';
    } else {
        content.style.display = 'none';
        button.textContent = 'Показать описание';
    }
}