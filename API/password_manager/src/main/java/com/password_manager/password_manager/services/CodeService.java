package com.password_manager.password_manager.services;

import com.password_manager.password_manager.Repositories.CodeRepository;
import com.password_manager.password_manager.enums.CodeContextEnum;
import com.password_manager.password_manager.models.CodeModel;
import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.producers.CodeMessage;
import com.password_manager.password_manager.services.utils.CodeUtils;
import jakarta.transaction.Transactional;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class CodeService {

    private final CodeRepository codeRepository;
    private final CodeUtils codeUtils;
    private final CodeMessage codeMessage;

    public CodeService(CodeRepository codeRepository, CodeUtils codeUtils, CodeMessage codeMessage) {
        this.codeRepository = codeRepository;
        this.codeUtils = codeUtils;
        this.codeMessage = codeMessage;
    }

    // sending mail messages
    public void publishCodeMessageEmail(UserModel userModel, CodeModel codeModel) {
        if (codeModel.getContext().equals(CodeContextEnum.EMAIL_CHANGE)) {
            this.codeMessage.publishChangeEmailMessageEmail(userModel, codeModel);
            return;
        }
        if (codeModel.getContext().equals(CodeContextEnum.FORGET_PASSWORD)) {
            this.codeMessage.publishChangePasswordMessageEmail(userModel, codeModel);
            return;
        }
        if (codeModel.getContext().equals(CodeContextEnum.DELETE)) {
            this.codeMessage.publishDeleteMessageEmail(userModel, codeModel);
            return;
        }
        this.codeMessage.publishLoginRequestMessageEmail(userModel, codeModel);
    }

    public void publishMessageEmailChanged(UserModel userModel, String new_email) {
        this.codeMessage.publishEmailChangedMessageEmail(userModel, new_email);
    }

    public void publishMessagePasswordChanged(UserModel userModel) {
        this.codeMessage.publishPasswordChangedMessageEmail(userModel);
    }

    public void publishDeleteMessageEmail(UserModel userModel, CodeModel codeModel) {
        this.codeMessage.publishDeleteMessageEmail(userModel, codeModel);
    }

    // requests
    @Transactional
    public void save(UserModel userModel, CodeContextEnum context) {
        CodeModel codeModel = this.codeRepository.save(this.codeUtils.createCode(userModel, context));
        this.publishCodeMessageEmail(userModel, codeModel);
    }

    public List<CodeModel> findByUserModel(UUID id) {
        return this.codeRepository.findByUserModel(id);
    }

    public Optional<CodeModel> findById(UUID id) {
        return this.codeRepository.findById(id);
    }

    public Optional<CodeModel> findByCode(String code) {
        return this.codeRepository.findByCode(code);
    }

    public void delete(CodeModel codeModel) {
        this.codeRepository.delete(codeModel);
    }

    public void deleteFromAccount(UserModel userModel) {
        List<CodeModel> codeModelList = this.findByUserModel(userModel.getId());
        codeModelList.forEach(this::delete);
    }
}
