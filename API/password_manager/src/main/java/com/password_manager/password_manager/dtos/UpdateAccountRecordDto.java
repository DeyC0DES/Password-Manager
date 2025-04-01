package com.password_manager.password_manager.dtos;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record UpdateAccountRecordDto(@NotNull @NotBlank String accountName,
                                     @NotNull @NotBlank String newUsername,
                                     @NotNull @NotBlank String newName,
                                     @NotNull @NotBlank String newPassword,
                                     @NotNull @NotBlank String icon,
                                     @NotNull Boolean favorite) {
}
