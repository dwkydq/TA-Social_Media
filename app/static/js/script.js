document.addEventListener('DOMContentLoaded', function() {
    
    // 1. PREVIEW FOTO PROFIL & COVER (Halaman Edit Profil)
    function setupImagePreview(inputId, imgPreviewId) {
        const inputElement = document.getElementById(inputId);
        const imgElement = document.getElementById(imgPreviewId);

        if (inputElement && imgElement) {
            inputElement.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        imgElement.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
    }
    setupImagePreview('cover-upload', 'cover-preview');
    setupImagePreview('pfp-upload', 'pfp-preview');


    // 2. PREVIEW MEDIA POSTINGAN (Gambar/Video di Beranda)
    // ============================================================
    const postFileInput = document.getElementById('file-upload');
    const postPreviewContainer = document.getElementById('media-preview');

    if (postFileInput && postPreviewContainer) {
        
        // A. Saat File Dipilih
        postFileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            
            if (file) {
                const fileUrl = URL.createObjectURL(file);
                let htmlContent = '';

                if (file.type.startsWith('image/')) {
                    htmlContent = `<img src="${fileUrl}" class="w-full rounded-xl border border-gray-700 object-cover max-h-[500px]">`;
                } else if (file.type.startsWith('video/')) {
                    htmlContent = `
                        <video controls class="w-full rounded-xl border border-gray-700 bg-black max-h-[500px]">
                            <source src="${fileUrl}">
                        </video>`;
                }

                htmlContent += `
                    <button type="button" class="btn-clear-preview absolute top-2 right-2 bg-black/70 hover:bg-black text-white rounded-full w-8 h-8 flex items-center justify-center transition backdrop-blur-sm shadow-lg border border-white/20">
                        <i class="fas fa-times pointer-events-none"></i>
                    </button>
                `;

                postPreviewContainer.innerHTML = htmlContent;
                postPreviewContainer.classList.remove('hidden');
            }
        });

        // B. Logic Tombol Hapus (Event Delegation)
        postPreviewContainer.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-clear-preview')) {
                postFileInput.value = '';
                postPreviewContainer.innerHTML = '';
                postPreviewContainer.classList.add('hidden'); 
            }
        });
    }


    // 3. LOGIKA TOMBOL SIDEBAR "POSTING BARU"
    const sidebarPostBtn = document.querySelector('.sidebar .btn-xyz');
    const postCaptionInput = document.getElementById('post-caption');
    const postCard = document.getElementById('create-post-card');

    if (sidebarPostBtn && postCaptionInput) {
        sidebarPostBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });

            setTimeout(() => {
                postCaptionInput.focus();
                if(postCard) {
                    postCard.classList.add('ring-4', 'ring-xyz-yellow');
                    setTimeout(() => {
                        postCard.classList.remove('ring-4', 'ring-xyz-yellow');
                    }, 1000);
                }
            }, 500);
        });
    }


    // 4. EMOJI PICKER (Beranda)
    const emojiBtn = document.querySelector('#emoji-btn');

    // Cek apakah tombol emoji ada DAN library EmojiButton sudah dimuat
    if (emojiBtn && postCaptionInput && typeof EmojiButton !== 'undefined') {
        
        // Inisialisasi Picker
        const picker = new EmojiButton({
            position: 'bottom-start', // Muncul di bawah tombol
            theme: 'dark',            // Tema gelap
            style: 'twemoji',         // Style emoji twitter (opsional)
            showPreview: false        // Sembunyikan preview besar di bawah
        });

        // Event saat emoji dipilih
        picker.on('emoji', selection => {
            postCaptionInput.value += selection.emoji;
            postCaptionInput.focus(); 
        });

        emojiBtn.addEventListener('click', () => {
            picker.togglePicker(emojiBtn);
        });
    }

});