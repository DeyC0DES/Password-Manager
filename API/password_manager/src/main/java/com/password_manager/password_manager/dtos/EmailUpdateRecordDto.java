package com.password_manager.password_manager.dtos;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record EmailUpdateRecordDto(@NotNull @NotBlank @Email String email,
                                   @NotNull @NotBlank String code,
                                   @NotNull @NotBlank @Email String new_email,
                                   @NotNull @NotBlank String new_username) {
}
