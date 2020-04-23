import axios from "axios";


export const JURUSAN_URL = "http://localhost:5000/api/kompetensi";


export default function getAllJurusan() {
    return axios.get(JURUSAN_URL);
}