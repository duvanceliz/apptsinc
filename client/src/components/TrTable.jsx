import toast from "react-hot-toast";
import { deleteOffer } from "../api/folder.api";
import { Navigate, useNavigate } from "react-router-dom";

export function TrTable({ project, triggerReloadOffers }) {

  const navigate = useNavigate()
  
  const handleBtnDelete = async (id) => {
    console.log(id);
    await deleteOffer(id)
    toast.success("Projecto eliminado")
    triggerReloadOffers()
     

  };

  return (
    <>
      <tr  >
        
        <th scope="row">{project.id}</th>
        <td>{project.name}</td>
        <td>{project.company_name}</td>
        <td>{project.nit}</td>
        <td>{project.asesor}</td>
        <td>{project.approved ? <p>aprobado</p> : <p>no aprobado</p>}</td>
        
        <td>
        <button className="btn btn-light btn-sm mx-2"
        onClick={()=>{
          navigate("/create-project/"+project.id)
        }}
        >Ver</button>
          <button
            className="btn btn-light btn-sm"
            onClick={() => handleBtnDelete(project.id)}
          >
            <i className="bi bi-trash"></i>
          </button>
          
        </td>
      </tr>
    </>
  );
}
