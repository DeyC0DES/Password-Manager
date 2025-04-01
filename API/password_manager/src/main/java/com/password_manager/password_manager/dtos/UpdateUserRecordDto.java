package com.password_manager.password_manager.dtos;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record UpdateUserRecordDto(@NotNull @NotBlank @Email String email,
                                  @NotNull @NotBlank String newUsername,
                                  @NotNull @Email String newEmail) {
}
