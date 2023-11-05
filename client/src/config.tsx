import { Patient } from "./types"

export const defaultPatients: Patient[] = [
    {
        slug: "john-doe",
        name: "John Doe",
        email: "johndoe@gmail.com",
        phone: "1234567890",
        status: "Deceased",
        dob: "01/01/1970",
        complaint: "Lung",
        imageUrl: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=6",    
    },
    {
        slug: "arnav-jain",
        name: "Arnav Jain",
        email: "arnavjain@gmail.com",
        phone: "1234567890",
        status: "Recovered",
        dob: "01/01/1970",
        complaint: "Breast",
        imageUrl: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60',
    },
    {
        slug: "joseph-cowles",
        name: "Joseph Cowles",
        email: "josephcowles@gmail.com",
        phone: "1234567890",
        status: "Undiagnosed",
        dob: "01/01/1970",
        complaint: "Lung",
        imageUrl: "https://images.unsplash.com/photo-1520813792240-56fc4a3765a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60",
    },
    {
        slug: "daniel-gorge",
        name: "Daniel Gorge",
        email: "danielgorge@gmail.com",
        phone: "1234567890",
        status: "Diagnosed",
        dob: "01/01/1970",
        complaint: "Breast",
        imageUrl: "https://images.unsplash.com/photo-1498551172505-8ee7ad69f235?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60",
    },
    {
        slug: "ahad-jawaid",
        name: "Ahad Jawaid",
        email: "ahadjawaid@gmail.com",
        phone: "1234567890",
        status: "Deceased",
        dob: "01/01/1970",
        complaint: "Lung",
        imageUrl: "https://images.unsplash.com/photo-1532417344469-368f9ae6d187?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60",
    }
]