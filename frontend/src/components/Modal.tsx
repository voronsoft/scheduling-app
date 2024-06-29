//import React from "react";
import {createPortal} from "react-dom";
import { SubmitHandler, useForm } from "react-hook-form";

type FormFields = {
  username: string;
  mail: string;
  password: string;
};

type ResponseToken = {
  access_token: string;
  token_type: string;
}
const GET_TOKEN_URL = `/api_admin/authorization`;

export default function Modal({open, onCloseClick}){
  const {
    register,
    reset,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<FormFields>();

  const onSubmit: SubmitHandler<FormFields> = async (data) => {
    console.log(data);

    try {
      const formData = new URLSearchParams();
        formData.append('username', data.username);
        formData.append('password', data.password);
      const response = await fetch(
        GET_TOKEN_URL,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData.toString(),
        }
      );
      if (response.ok) {
        // Обработка успешного ответа от сервера
        console.log("Request sent successfully!");
        console.log(response)
        const token = (await response.json()) as ResponseToken;
        console.log(token);
        // Очистить значения ввода в форме
        reset();
        //setSelectedDate(""); // Сбросить форму
      } else {
        // Обработка ошибки от сервера
        console.error("Request failed:", response.statusText);
        throw new Error();
      }
    } catch(error) {
      console.error("Request error:", error);
      setError("root", {
        message: "Something went wrong, please refresh the page and try again",
      });
    }
  };

  if(open === false) return null
  return  (
    <>
      {createPortal(
        <div className="modal-wrapper">
          <div className="diagonal modal flex flex-col">
              <button onClick={onCloseClick} className="bg-black text-white p-3 self-end">Close</button>
              <div className="mt-5">
                <form 
                  autoComplete="off"
                  onSubmit={handleSubmit(onSubmit)}
                  className="flex flex-col gap-5"
                >
                  <input
                    {...register("username", { required: "Please enter your username" })}
                    type="text"
                    placeholder="Enter username"
                    className="p-2 rounded-md text-black w-full"
                  />
                  {errors.username && (
                    <div className="text-red-500">{errors.username.message}</div>
                  )}
                  <input
                    {...register("mail", { 
                      required: "Please enter your email", 
                      //pattern: /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, 
                    })}
                    type="text"
                    placeholder="Enter mail"
                    className="p-2 rounded-md text-black w-full"
                  />
                  {errors.mail && (
                    <div className="text-red-500">{errors.mail.message}</div>
                  )}
                  <input
                    {...register("password", { required: "Please enter your password" })}
                    type="text"
                    placeholder="Enter password"
                    className="p-2 rounded-md text-black w-full"
                  />
                  {errors.password && (
                    <div className="text-red-500">{errors.password.message}</div>
                  )}
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="bg-amber-400 p-2 rounded-md"
                  >
                    {isSubmitting ? "Loading" : "Submit"}
                  </button>
                </form>
              </div>             
          </div>
        </div> ,
        document.body
      )}
    </>
  )  
}

