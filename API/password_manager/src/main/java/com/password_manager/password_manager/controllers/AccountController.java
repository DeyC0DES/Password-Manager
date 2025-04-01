package com.password_manager.password_manager.controllers;

import com.password_manager.password_manager.dtos.*;
import com.password_manager.password_manager.models.AccountModel;
import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.services.AccountService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.encrypt.TextEncryptor;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("passwordManager/api/account")
public class AccountController {

    private final AccountService accountService;
    private final TextEncryptor textEncryptor;

    public AccountController(AccountService accountService, TextEncryptor textEncryptor) {
        this.accountService = accountService;
        this.textEncryptor = textEncryptor;
    }

    @PostMapping("/create")
    public ResponseEntity<Object> createAccount(@RequestBody @Valid AccountCreateRecordDto body) {
        return this.findAccount(body.name())
                .<ResponseEntity<Object>>map(account -> {
                    if (account.getUserModel().getId() == this.getAuthenticationAccount().getId() && account.getAccountName().equals(body.name())) {
                        return ResponseEntity.status(HttpStatus.CONFLICT).body(new ApiResponseRecordDto("Already have an account with that name", null));
                    }
                    return this.createAndSaveAccount(body);
                })
                .orElseGet(() -> {
                    return this.createAndSaveAccount(body);
                });
    }

    @GetMapping("/getAccounts")
    public ResponseEntity<Object> getAll() {
        return ResponseEntity.ok(new ApiResponseRecordDto(null, this.accountService.findByUserModel(this.getAuthenticationAccount().getId())));
    }

    @GetMapping("/decode/password")
    public ResponseEntity<Object> getPassword(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.findAccount(body.item1())
                .<ResponseEntity<Object>>map(account -> {
                    if (account.getUserModel().getId().equals(this.getAuthenticationAccount().getId())) {
                        return ResponseEntity.ok(new ApiResponseRecordDto(this.decode(account.getAccountPassword()), null));
                    }
                    return this.differentIds();

                })
                .orElseGet(this::notFoundResponse);
    }

    @PutMapping("/update")
    public ResponseEntity<Object> update(@RequestBody @Valid UpdateAccountRecordDto body) {
        return this.findAccount(body.accountName())
                .<ResponseEntity<Object>>map(account -> this.updateAndSaveAccount(body))
                .orElseGet(this::notFoundResponse);
    }

    @PutMapping("/update/fav")
    public ResponseEntity<Object> updateFav(@RequestBody @Valid UpdateFavRecordDto body) {
        return this.findAccount(body.name())
                .<ResponseEntity<Object>>map(account -> {
                    if (!account.getUserModel().getId().equals(this.getAuthenticationAccount().getId())) {
                        return this.differentIds();
                    }
                    return this.updateFav(account, body);
                })
                .orElseGet(this::notFoundResponse);
    }

    @DeleteMapping("/delete")
    public ResponseEntity<Object> delete(@RequestBody @Valid ApiRequestRecordDto body) {
        return this.findAccount(body.item1())
                .<ResponseEntity<Object>>map(account -> {
                    if (account.getUserModel().getId().equals(this.getAuthenticationAccount().getId())) {
                        return this.accountService.delete(account);
                    }
                    return this.differentIds();
                })
                .orElseGet(this::notFoundResponse);
    }

    // method
    public String decode(String text) {
        return textEncryptor.decrypt(text);
    }

    public String encode(String text) {
        return textEncryptor.encrypt(text);
    }

    public String verify_parameters(String value1, String value2) {
        return (!value1.equals(value2) ? value1 : value2);
    }

    public UserModel getAuthenticationAccount() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return (UserModel) authentication.getPrincipal();
    }

    public Optional<AccountModel> findAccount(String accountName) {
        return this.accountService.findByAccountName(accountName);
    }

    public ResponseEntity<Object> updateFav(AccountModel account, UpdateFavRecordDto data) {
        account.setFavorite(data.fav());
        this.accountService.save(account);
        return ResponseEntity.ok(new ApiResponseRecordDto("Changed!", null));
    }

    public ResponseEntity<Object> updateAndSaveAccount(UpdateAccountRecordDto data) {
        Optional<AccountModel> accountModelOptional = this.findAccount(data.accountName());

        if (accountModelOptional.isEmpty()) {
            return this.notFoundResponse();
        }

        if (!accountModelOptional.get().getUserModel().getId().equals(this.getAuthenticationAccount().getId())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ApiResponseRecordDto(ResponseMessages.ACCOUNT_NOT_FOUND, ""));
        }

        AccountModel accountModel = accountModelOptional.get();
        accountModel.setAccountName(verify_parameters(data.newName(), accountModel.getAccountName()));
        accountModel.setAccountUserName(verify_parameters(data.newUsername(), accountModel.getAccountUserName()));
        accountModel.setOldAccountPassword(!this.decode(accountModel.getAccountPassword()).equals(data.newPassword()) ? this.decode(accountModel.getAccountPassword()) : accountModel.getOldAccountPassword());
        accountModel.setAccountPassword(this.encode(verify_parameters(data.newPassword(), this.decode(accountModel.getAccountPassword()))));
        accountModel.setFavorite(data.favorite() != accountModel.getFavorite() ? data.favorite() : accountModel.getFavorite());
        this.accountService.save(accountModel);
        return ResponseEntity.ok(new ApiResponseRecordDto("Account updated with successfully!", null));
    }

    public ResponseEntity<Object> notFoundResponse() {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiResponseRecordDto(ResponseMessages.ACCOUNT_NOT_FOUND, null));
    }

    public ResponseEntity<Object> differentIds() {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ApiResponseRecordDto(ResponseMessages.ACCOUNT_NOT_FOUND, null));
    }

    public ResponseEntity<Object> createAndSaveAccount(AccountCreateRecordDto data) {
        AccountModel accountModel = new AccountModel();
        accountModel.setIcon(data.icon());
        accountModel.setAccountName(data.name());
        accountModel.setAccountUserName(data.username());
        accountModel.setAccountPassword(this.encode(data.password()));
        accountModel.setOldAccountPassword(null);
        accountModel.setUserModel(this.getAuthenticationAccount());
        accountModel.setFavorite(data.fav());
        this.accountService.save(accountModel);
        return ResponseEntity.ok(new ApiResponseRecordDto("Account registred successfully!", null));
    }
}
