// Funcionalidad del chatbot
document.addEventListener('DOMContentLoaded', function() {
    const chatbot = document.getElementById('chatbot');
    
    if (chatbot) {
        const chatInput = chatbot.querySelector('#chat-input');
        const chatSend = chatbot.querySelector('#chat-send');
        const chatMessages = chatbot.querySelector('#chat-messages');
        
        chatSend.addEventListener('click', enviarMensaje);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                enviarMensaje();
            }
        });
        
        function enviarMensaje() {
            const mensaje = chatInput.value.trim();
            if (mensaje) {
                agregarMensaje('usuario', mensaje);
                chatInput.value = '';
                
                // Enviar al servidor
                fetch('/chatbot/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({pregunta: mensaje})
                })
                .then(response => response.json())
                .then(data => {
                    agregarMensaje('bot', data.respuesta);
                });
            }
        }
        
        function agregarMensaje(tipo, texto) {
            const mensajeDiv = document.createElement('div');
            mensajeDiv.className = `mensaje ${tipo}`;
            mensajeDiv.textContent = texto;
            chatMessages.appendChild(mensajeDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]').value;
        }
    }
});

// Cálculo de calorías (fórmula básica)
function calcularCaloriasBasales(genero, peso, altura, edad, actividad, objetivo) {
    let tmb;
    
    if (genero === 'M') {
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad);
    } else {
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad);
    }
    
    const factoresActividad = {
        'sedentario': 1.2,
        'ligero': 1.375,
        'moderado': 1.55,
        'intenso': 1.725,
        'atleta': 1.9
    };
    
    let calorias = tmb * factoresActividad[actividad];
    
    // Ajustar según objetivo
    if (objetivo === 'perder') {
        calorias -= 500;
    } else if (objetivo === 'ganar') {
        calorias += 500;
    }
    
    return Math.round(calorias);
}