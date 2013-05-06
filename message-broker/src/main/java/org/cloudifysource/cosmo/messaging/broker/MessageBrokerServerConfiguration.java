/*******************************************************************************
 * Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

package org.cloudifysource.cosmo.messaging.broker;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Creates a new {@link MessageBrokerServer}.
 *
 * @author Dan Kilman
 * @since 0.1
 */
@Configuration
public class MessageBrokerServerConfiguration {

    @Value("${message-broker.port}")
    int port;

    @Bean(initMethod = "start", destroyMethod = "stop")
    public MessageBrokerServer messageBrokerServer() {
        return new MessageBrokerServer(port);
    }

}