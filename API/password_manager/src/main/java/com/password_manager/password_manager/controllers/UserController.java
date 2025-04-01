package com.password_manager.password_manager.controllers;

import com.password_manager.password_manager.config.security.TokenService;
import com.password_manager.password_manager.dtos.*;
import com.password_manager.password_manager.enums.CodeContextEnum;
import com.password_manager.password_manager.enums.CodeStatsEnum;
import com.password_manager.password_manager.enums.RequestTypeEnum;
import com.password_manager.password_manager.enums.RoleEnum;
import com.password_manager.password_manager.models.CodeModel;
import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.services.CodeService;
import com.password_manager.password_manager.services.UserServices;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.encrypt.TextEncryptor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("passwordManager/api/user")
public class UserController {

    private final UserServices userServices;
    private final TokenService tokenService;
    private final PasswordEncoder passwordEncoder;
    private final CodeService codeService;

    public UserController(UserServices userServices, TokenService tokenService, PasswordEncoder passwordEncoder, CodeService codeService, TextEncryptor textEncryptor, ResponseMessages responseMessages1) {
        this.userServices = userServices;
        this.tokenService = tokenService;
        this.passwordEncoder = passwordEncoder;
        this.codeService = codeService;
    }

    // end points

    @PostMapping("/register")
    public ResponseEntity<Object> register(@RequestBody @Valid RegisterRecordDto body) {
        if (!body.password().equals(body.cPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ApiResponseRecordDto("Password does not match!", null));
        }
        return this.userServices.findByEmail(body.email())
                .<ResponseEntity<Object>>map(account -> ResponseEntity.status(HttpStatus.CONFLICT).body(new ApiResponseRecordDto("Already have an account with that email!", null)))
                .orElseGet(() -> this.createAccountAndSave(body));
    }

    @PostMapping("/login")
    public ResponseEntity<Object> login(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.userServices.findByEmail(body.item1())
                .<ResponseEntity<Object>>map(account -> {
                    if (passwordEncoder.matches(body.item2(), account.getPassword())) {
                        return this.createAndSendCode(account, CodeContextEnum.LOGIN);
                    }
                    return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ApiResponseRecordDto(ResponseMessages.WRONG_PASSWORD, null));
                })
                .orElseGet(this::notFoundResponse);
    }

    @PostMapping("/forget")
    public ResponseEntity<Object> forgetPassword(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.findUser(body.item1())
                .<ResponseEntity<Object>>map(account -> this.createAndSendCode(account, CodeContextEnum.FORGET_PASSWORD))
                .orElseGet(this::notFoundResponse);
    }

    @PostMapping("/2steps/sendCodeAgain")
    public ResponseEntity<Object> sendCode(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.userServices.findByEmail(body.item1())
                .<ResponseEntity<Object>>map(account -> this.createAndSendCode(account, CodeContextEnum.LOGIN))
                .orElseGet(this::notFoundResponse);
    }

    @PostMapping("/2steps/verification")
    public ResponseEntity<Object> stepsVerification(@RequestBody @Valid ApiRequestRecordDto body) {
        Optional<UserModel> userModelOptional = this.findUser(body.item1());
        CodeModel codeModel = (CodeModel) this.findCode(body.item2());

        if (userModelOptional.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.USER_NOT_FOUND, null));
        }

        if (codeModel == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
        }

        return this.verifyCode(this.codeService.findByCode(body.item2()), userModelOptional.get(), RequestTypeEnum.LOGIN, null);
    }

    @PostMapping("/settings/verification")
    public ResponseEntity<Object> emailVerification(@RequestBody @Valid EmailUpdateRecordDto body) {
        Optional<UserModel> userModelOptional = this.findUser(body.email());
        CodeModel codeModel = (CodeModel) this.findCode(body.code());

        if (userModelOptional.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.USER_NOT_FOUND, null));
        }

        if (codeModel == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
        }

        return this.verifyCode(this.codeService.findByCode(body.code()), userModelOptional.get(), RequestTypeEnum.CHANGE_EMAIL, body);
    }

    @PostMapping("/forget/verification")
    public ResponseEntity<Object> forgetVerification(@RequestBody @Valid ApiRequestRecordDto body) {
        Optional<UserModel> userModelOptional = this.findUser(body.item1());
        CodeModel codeModel = (CodeModel) this.findCode(body.item2());

        if (userModelOptional.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.USER_NOT_FOUND, null));
        }

        if (codeModel == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
        }

        return this.verifyCode(this.codeService.findByCode(body.item2()), userModelOptional.get(), RequestTypeEnum.FORGET, null);
    }

    @PostMapping("/delete/send-code")
    public ResponseEntity<Object> deleteCodeSend(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.findUser(body.item1())
                .<ResponseEntity<Object>>map(account -> this.createAndSendCode(account, CodeContextEnum.DELETE))
                .orElseGet(this::notFoundResponse);
    }

    @PutMapping("/update")
    public ResponseEntity<Object> update(@RequestBody @Valid UpdateUserRecordDto body) {
        return this.findUser(body.email())
                .<ResponseEntity<Object>>map(account -> this.updateAndSaveAccount(body))
                .orElseGet(this::notFoundResponse);
    }

    @PutMapping("/update/password")
    public ResponseEntity<Object> updatePassword(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.findUser(body.item1())
                .<ResponseEntity<Object>>map(account -> updatePassword(account, body.item2()))
                .orElseGet(this::notFoundResponse);
    }

    @DeleteMapping("/delete/verification")
    public ResponseEntity<Object> deleteVerification(@RequestBody @Valid ApiRequestRecordDto body) {
        Optional<UserModel> userModelOptional = this.findUser(body.item1());
        CodeModel codeModel = (CodeModel) this.findCode(body.item2());

        if (userModelOptional.isEmpty()) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.USER_NOT_FOUND, null));
        }

        if (codeModel == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
        }

        return this.verifyCode(this.codeService.findByCode(body.item2()), userModelOptional.get(), RequestTypeEnum.DELETE, null);
    }

    // methods
    public String verify_parameters(String value1, String value2) {
        return (!value1.equals(value2) ? value1 : value2);
    }

    public CodeModel findCode(String code) {
        if (this.codeService.findByCode(code).isPresent()) {
            return this.codeService.findByCode(code).get();
        }
        return null;
    }

    public UserModel getAuthenticationAccount() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return (UserModel) authentication.getPrincipal();
    }

    public Optional<UserModel> findUser(String email) {
        return this.userServices.findByEmail(email);
    }

    public ResponseEntity<Object> updatePassword(UserModel userModel, String password) {
        userModel.setPassword(passwordEncoder.encode(password));
        this.userServices.update(userModel);
        this.codeService.publishMessagePasswordChanged(userModel);
        return ResponseEntity.ok("Password changed");
    }

    public ResponseEntity<Object> createAndSendCode(UserModel userModel, CodeContextEnum context) {
        this.codeService.save(userModel, context);
        return ResponseEntity.ok("Code will be send to your email!!!");
    }

    public ResponseEntity<Object> verifyCode(Optional<CodeModel> codeModelOptional, UserModel userModel, RequestTypeEnum requestType, EmailUpdateRecordDto data) {

        if (codeModelOptional.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
        }

        if (codeModelOptional.get().getStats().equals(CodeStatsEnum.DISABLED)) {
            this.codeService.delete(codeModelOptional.get());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ApiResponseRecordDto(ResponseMessages.CODE_EXPIRE, null));
        }

        if (codeModelOptional.get().getUserModel().getId() == userModel.getId()) {
            this.codeService.deleteFromAccount(userModel);

            switch (codeModelOptional.get().getContext()) {
                case CodeContextEnum.LOGIN -> {
                    if (requestType.equals(RequestTypeEnum.LOGIN)) {
                        this.userServices.publishLoginMessage(userModel);
                        return ResponseEntity.ok(new ApiResponseRecordDto(this.tokenService.generateToken(userModel), userModel.getUsername()));
                    }
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto("Invalid code", null));
                }

                case CodeContextEnum.EMAIL_CHANGE -> {
                    if (requestType.equals(RequestTypeEnum.CHANGE_EMAIL)) {
                        this.codeService.publishMessageEmailChanged(userModel, data.new_email());
                        userModel.setUsername(data.new_username());
                        userModel.setEmail(data.new_email());
                        this.userServices.update(userModel);
                        return ResponseEntity.ok(new ApiResponseRecordDto("Email changed!", null));
                    }
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto("Invalid code", null));
                }

                case CodeContextEnum.FORGET_PASSWORD -> {
                    if (requestType.equals(RequestTypeEnum.FORGET)) {
                        return ResponseEntity.ok(new ApiResponseRecordDto("Code valid", this.tokenService.generateToken(userModel)));
                    }
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto("Invalid code", null));
                }

                case CodeContextEnum.DELETE -> {
                    if (requestType.equals(RequestTypeEnum.DELETE)) {
                        this.userServices.delete(userModel);
                        return ResponseEntity.ok(new ApiResponseRecordDto("Account Deleted", null));
                    }
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto("Invalid code", null));
                }
            }

            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
        }
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ApiResponseRecordDto(ResponseMessages.CODE_INVALID, null));
    }

    public ResponseEntity<Object> createAccountAndSave(RegisterRecordDto data) {
        UserModel model = new UserModel();
        model.setUsername(data.username());
        model.setEmail(data.email());
        model.setPassword(this.passwordEncoder.encode(data.password()));
        model.setRole(RoleEnum.USER);
        this.userServices.save(model);
        return ResponseEntity.ok(new ApiResponseRecordDto("Your account has been created!", null));
    }

    public ResponseEntity<Object> updateAndSaveAccount(UpdateUserRecordDto data) {
        Optional<UserModel> userModelOptional = this.findUser(data.email());

        if (userModelOptional.isEmpty()) {
            this.notFoundResponse();
        }

        UserModel userModel = userModelOptional.get();

        if (!this.getAuthenticationAccount().getId().equals(userModel.getId())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Something went wrong!");
        }

        userModel.setUsername(verify_parameters(data.newUsername(), userModel.getUsername()));

        if (!userModel.getEmail().equals(data.newEmail())) {
            this.createAndSendCode(this.getAuthenticationAccount(), CodeContextEnum.EMAIL_CHANGE);
            return ResponseEntity.status(HttpStatus.ACCEPTED).body(new ApiResponseRecordDto("Account updated successfully", null));
        }

        this.userServices.save(userModel);
        return ResponseEntity.ok(new ApiResponseRecordDto("Account updated successfully", null));
    }

    public ResponseEntity<Object> notFoundResponse() {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiResponseRecordDto(ResponseMessages.USER_NOT_FOUND, null));
    }

}