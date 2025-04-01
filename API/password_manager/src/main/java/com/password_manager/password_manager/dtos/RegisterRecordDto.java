package com.password_manager.password_manager.dtos;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record RegisterRecordDto(@NotNull @NotBlank String username,
                                @NotNull @NotBlank @Email String email,
                                @NotNull @NotBlank String password,
                                @NotNull @NotBlank String cPassword) {
}
