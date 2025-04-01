package com.password_manager.password_manager.dtos;

import org.springframework.stereotype.Component;

@Component
public class ResponseMessages {
    public static final String WRONG_PASSWORD = "The password does not matches";
    public static final String USER_NOT_FOUND = "The email its invalid!";
    public static final String ACCOUNT_NOT_FOUND = "This account is invalid or dont exist";
    public static final String CODE_INVALID = "Invalid code!";
    public static final String CODE_EXPIRE = "Expired code!";
}
