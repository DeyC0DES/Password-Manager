package com.password_manager.password_manager.dtos;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record AccountCreateRecordDto(@NotNull @NotBlank String name,
                                     @NotNull @NotBlank String username,
                                     @NotNull @NotBlank String password,
                                     @NotNull @NotBlank String icon,
                                     boolean fav) {
}
