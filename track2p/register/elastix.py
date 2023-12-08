import itk

def reg_img_elastix(ref_img, mov_img, track_ops):
    # convert to itk images
    ref_img_itk = itk.GetImageFromArray(ref_img)
    mov_img_itk = itk.GetImageFromArray(mov_img)

    # import default parameter map
    parameter_object = itk.ParameterObject.New()
    parameter_map = parameter_object.GetDefaultParameterMap(track_ops.transform_type)
    parameter_object.AddParameterMap(parameter_map)

    # call registration function
    mov_img_reg_itk, reg_params = itk.elastix_registration_method(
        ref_img_itk,
        mov_img_itk,
        parameter_object = parameter_object
    )

    # convert back to numpy array
    mov_img_reg = itk.GetArrayFromImage(mov_img_reg_itk)
    reg_params.SetParameter("FinalBSplineInterpolationOrder", "0")

    return mov_img_reg, reg_params