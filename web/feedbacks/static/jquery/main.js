console.log("HELLO")

const circleform = document.getElementById("circle-form")

const circlesDataBox = document.getElementById("circles-data-box")
const circlesInput = document.getElementById("circles")

const ssasDataBox = document.getElementById("ssas-data-box")
const ssasInput = document.getElementById("ssas")

const btnBox = document.getElementById("btn-box")
const alertBox = document.getElementById("alert-box")

const circleText = document.getElementById("circle-text")
const ssaText = document.getElementById("ssa-text")

const csrf = document.getElementsByName('csrfmiddlewaretoken')

$.ajax({
    type: 'GET',
    url: '/home/circles-json/',
    success: function(response){
        console.log(response.data)
        const circlesData = response.data
        circlesData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class', 'item')
            option.setAttribute('data-value', item.name)
            circlesDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})

circlesInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedCircle = e.target.value

    ssasDataBox.innerHTML = ""
    ssaText.textContent = "SSA"
    ssaText.classList.add("default")

    $.ajax({
        type: 'GET',
        url: '/home/ssa-json/' + selectedCircle,
        success: function(response){
            console.log(response.data)
            const ssasData = response.data
            ssasData.map(item=>{
                const option = document.createElement('div')
                option.textContent = item.name
                option.setAttribute('class', 'item')
                option.setAttribute('data-value', item.name)
                ssasDataBox.appendChild(option)
            })
            
            ssasInput.addEventListener('change', e=>{
                console.log(e.target.value)
                const selectedSsa = e.target.value
                btnBox.classList.remove('not-visible')
            })
        },
        error: function(error){
            console.log(error)
        }
    })

})

circleform.addEventListener('submit', e=>{
    e.preventDefault()
    console.log("submitted")
    

})