const image = document.querySelector('.image');
const hover = document.querySelector('.hover');
const modal = document.getElementById('profileModal');
const close = document.querySelector('.close');

/* function show() {
    hover.classList.add('active');
    modal.classList.add('show');
}

function hide() {
    hover.classList.remove('active');
    modal.classList.remove('show');
}

image.addEventListener('click', show);
close.addEventListener('click', hide);

document.addEventListener('DOMContentLoaded', function() {
    var profileImage = document.getElementById('profileImage');
    var imageContainer = document.querySelector('.image');
    if (profileImage && imageContainer) {
        imageContainer.style.backgroundImage = 'url(' + profileImage.src + ')';
    }
}); */

document.addEventListener('DOMContentLoaded', function() {
    var bioText = document.getElementById('bioText');
    var seeMoreLink = document.getElementById('seeMoreLink');
    var seeLessLink = document.getElementById('seeLessLink');
    var contentDiv = document.querySelector('.content');

    var fullBio = bioText.innerText;
    var words = fullBio.split(' ');

    if (words.length > 25) {
        var truncatedBio = words.slice(0, 25).join(' ') + '... ';
        bioText.innerText = truncatedBio;
        bioText.appendChild(seeMoreLink);
        seeMoreLink.style.display = 'inline';

        seeMoreLink.addEventListener('click', function(event) {
            event.preventDefault();
            bioText.innerText = fullBio + ' ';
            bioText.appendChild(seeLessLink);
            contentDiv.classList.add('expanded');
            seeMoreLink.style.display = 'none';
            seeLessLink.style.display = 'inline';
        });

        seeLessLink.addEventListener('click', function(event) {
            event.preventDefault();
            bioText.innerText = truncatedBio;
            bioText.appendChild(seeMoreLink);
            contentDiv.classList.remove('expanded');
            seeMoreLink.style.display = 'inline';
            seeLessLink.style.display = 'none';
        });
    }
});

function openProfileModal() {
    document.getElementById('profileModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const image = document.querySelector('.image');
    const close = document.querySelector('.close');

    if (image) {
        image.addEventListener('click', openProfileModal);
    }

    if (close) {
        close.addEventListener('click', function() {
            closeModal('profileModal');
        });
    }
});