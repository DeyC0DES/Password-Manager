package com.password_manager.password_manager.config.security;

import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.services.UserServices;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserServices userServices;

    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserModel userModel =this.userServices.findByEmail(username).orElseThrow(() -> new UsernameNotFoundException(""));
        return new User(userModel.getEmail(), userModel.getPassword(), new ArrayList<>());
    }


}
