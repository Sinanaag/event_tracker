// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Update job status via API
async function updateJobStatus(jobId, newStatus) {
    try {
        const response = await fetch('/update-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                job_id: jobId,
                new_status: newStatus
            })
        });

        const data = await response.json();
        if (data.success) {
            console.log('Status updated successfully');
            location.reload(); // Reload to show updated status
        } else {
            alert('Failed to update status');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating status');
    }
}

// Add drag and drop functionality when page loads
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    let draggedCard = null;

    cards.forEach(card => {
        card.draggable = true;
        
        card.addEventListener('dragstart', function(e) {
            draggedCard = this;
            this.style.opacity = '0.5';
        });

        card.addEventListener('dragend', function(e) {
            this.style.opacity = '1';
        });
    });

    const columns = document.querySelectorAll('.column');
    columns.forEach(column => {
        column.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.backgroundColor = 'rgba(59, 130, 246, 0.1)';
        });

        column.addEventListener('dragleave', function(e) {
            this.style.backgroundColor = '';
        });

        column.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.backgroundColor = '';
            
            if (draggedCard && draggedCard.dataset.jobId) {
                const newStatus = this.dataset.status;
                updateJobStatus(draggedCard.dataset.jobId, newStatus);
            }
        });
    });
});
