import React from 'react'
import uploadSVG from '../assets/uploadImage.svg'
/*import { useFormUpload } from '../components/useFormUpload'*/
import { useDropzone } from 'react-dropzone'

export default function Upload() {

    /*const { file, prediction, description, isLoading, onDrop } =
        useFormUpload()*/

    const { getRootProps, getInputProps, isDragActive } =
        useDropzone({ onDrop, accept: 'image/jpeg, image/png, image/jpg, image/tif' })

    return (

        <div>
             (  <div className="grid place-items-center">

                    <div className="grid place-items-center py-5">
                        <div className="flex flex-row text-5xl font-bold text-[#246125]">Check Diseases</div>
                        <div className='bg-lime-500 h-1 w-36 my-2 rounded-lg'></div>
                    </div>

                    <div className="py-6">
                        <input {...getInputProps()} data-testid="upload-image" />
                        <h2 className='text-center text-3xl py-5'>Choose a file</h2>

                        {isDragActive ? (
                            <div className='w-96 h-96 rounded-lg mb-24 bg-gray-400 border-4 border-dashed border-[#1E1E1E] grid place-items-center' data-testid="dropzone-container"  {...getRootProps()}>
                                <img src={uploadSVG} className="w-28 h-28 pt-8" alt="Illustration upload" />
                                <h1 className="text-[28px] font-bold text-center">Drop here</h1>
                                <h1 className="text-xl">to send your photo</h1>
                            </div>
                        ) : (
                            <div className='w-96 h-96 rounded-lg mb-24 bg-gray-400 border-4 border-dashed border-[#1E1E1E] grid place-items-center' data-testid="dropzone-container"  {...getRootProps()}>
                                <img src={uploadSVG} className="w-28 h-28 pt-8" alt="Illustration upload" />
                                <h1 className="text-[28px] font-bold text-center">Drag and Drop or click here</h1>
                                <h1 className="text-xl">to send your photo</h1>
                                <p className='text-lg pb-14'>No file selected.</p>
                            </div>
          
                            <div className="">
                        <button className='bg-secondary py-2 px-8 rounded-md text-xl text-white' {...getRootProps()}>
                            Upload image
                        </button>
                        <input {...getInputProps()} />
                    </div> 
                        )}
                      
                    </div>
                </div>
            )}

        </div>
    )
}
