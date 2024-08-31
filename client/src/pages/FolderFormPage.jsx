import { useForm } from "react-hook-form";
import { createFolder, deleteFolder, getFolder,updateFolder } from "../api/folder.api";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect } from "react";
import { toast } from 'react-hot-toast'
export function FolderFormPage() {
  const navigate = useNavigate();
  const params = useParams();


  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue
  } = useForm();

  const onSubmit = handleSubmit(async (data) => {
    if (params.id) { 
       
      await updateFolder(params.id,data);
      toast.success("Carpeta Actulizada",{
        position: "bottom-right"
      })

    } else {
      await createFolder(data);
      toast.success("Carpeta creada",{
        position: "bottom-right"
      })
    }
    navigate("/home");
  });

  useEffect(()=>{

    async function loadFolder(){
        if(params.id){
            const {data} = await getFolder(params.id)
            setValue('name',data.name)
           
         }
    }
    loadFolder()

  },[])


  

  return (
    <div>
      <div className="container">
        <div className="row">
          <div className="col-md-4"></div>
          <div className="col-md-4">
            <div className="card">
              <div className="card-header">
                <div className="row g-3">
                  <div className="col-6">
                    <p className="fs-4">Crear carpeta</p>
                  </div>
                  <div className="col-6 text-end">
                    {params.id && (
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={async () => {
                          const res = window.confirm("Estas seguro?");
                          if (res) {
                            await deleteFolder(params.id);
                            toast.success("Carpeta eliminada",{
                                position: "bottom-right"
                              })
                            navigate("/home/");
                          }
                        }}
                      >
                        <i className="bi bi-trash"></i>
                      </button>
                    )}
                  </div>
                </div>
              </div>
              <div className="card-body">
                <form onSubmit={onSubmit}>
                  <div className="mb-4">
                    {errors.name && (
                      <div className="alert alert-danger">
                        Este campo es requerido
                      </div>
                    )}
                  </div>
                  <div className="mb-3">
                    <input
                      className="form-control"
                      type="text"
                      placeholder="Nombre"
                      {...register("name", { required: true })}
                     
                    />
                  </div>
                  <button className="btn btn-primary w-100">Guardar</button>
                </form>
              </div>
            </div>
          </div>
          <div className="col-md-4"></div>
        </div>
      </div>
    </div>
  );
}
