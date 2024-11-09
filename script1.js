document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const fullName = document.getElementById("fullName").value.trim();
    const serverURL = 'http://localhost:3000/upload';


    if (!fullName) {
        alert("Пожалуйста, введите ваше полное имя.");
        return;
    }

 
    const data = { fullName };

    try {
        const response = await fetch(serverURL, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), 
        });

        if (!response.ok) {
            let errorMessage = `HTTP error! status: ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage += `, message: ${errorData.message || 'Неизвестная ошибка'}`;
            } catch (jsonError) {

            }
            throw new Error(errorMessage);
        }

        const responseData = await response.json();
        alert(responseData.message); 

    } catch (error) {
        console.error('Error:', error);
        alert(`Произошла ошибка: ${error.message}`); 
    }
});