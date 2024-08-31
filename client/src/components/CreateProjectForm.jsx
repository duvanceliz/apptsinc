import { useForm } from "react-hook-form";
import { createProject, getProject } from "../api/folder.api";
import { useNavigate, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import { useEffect, useState } from "react";

export function CreateProjectForm() {
  const navigate = useNavigate()
  const {id} = useParams()
  const [project, setProject] = useState(null)
  

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm();

  const onSubmit = handleSubmit( async (data) => {
    await createProject(data)
    toast.success("Proyecto Creado")

    navigate("/show-all-offers/")

  });

  useEffect(()=>{

    async function loadProject(){
    
      if(id){
        
  
        const {data} =  await getProject(id)
  
        setValue('name',data.name)
        setValue('company_name',data.company_name)
        setValue('nit',data.nit)
        setValue('asesor',data.asesor)
        setProject(data)
            
      
      }
    
    }
    
    loadProject()
  },[]);
   
 
  
  return (
    <div className="card">
      <div className="card-header">Crear un proyecto</div>
      <div className="card-body">
        <form action="" onSubmit={onSubmit}>
          {errors.name && (
            <div className="alert alert-danger">Este campo es requerido</div>
          )}

          <div className="mb-3">
          <label htmlFor="" id="name">
            Nombre del proyecto:
          </label>
          <input
            type="text"
            className="form-control"
            id="name"
            {...register("name", { required: true })}
          />
          </div>
          <div className="mb-3">
          <label htmlFor="" id="company">
            Nombre de la empresa:
          </label>
          <input
            type="text"
            className="form-control"
            id="company"
            {...register("company_name", { required: true })}
          />
          </div>
         <div className="mb-3">
         <label htmlFor="" id="nit">
            NIT:
          </label>
          <input
            type="text"
            className="form-control"
            id="nit"
            {...register("nit", { required: true })}
          />
         </div>
           {id ? (<p className="form-control">{ project  && project.asesor}</p>):(<div className="mb-3">
            <select name="" id="" className="form-control"
            {...register("asesor", { required: true })}
            >
              <option value="Duvan Celiz">Duvan Celiz</option>
              <option value="Juanito Perez">Juanito Perez</option>
              <option value="Pepito Alvarez">Pepito Alvarez</option>
            </select>
          </div>)}
          

          <button className="btn btn-primary w-100">Enviar</button>
        </form>
      </div>
    </div>
  );
}
